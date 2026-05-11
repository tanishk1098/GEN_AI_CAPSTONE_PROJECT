"""LangGraph-powered self-healing workflow for Snowflake ETL errors."""

from __future__ import annotations

import logging
import os
from typing import Literal, TypedDict

# from langchain_xai import ChatXAI
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from self_healing_agent_B3.mcp_tools import (
    SnowflakeMCPTools,
)

logger = logging.getLogger("self_healing_agent")

if not logger.handlers:

    os.makedirs("/opt/airflow/logs", exist_ok=True)

    file_handler = logging.FileHandler(
        "/opt/airflow/logs/agent_diagnostics.log"
    )

    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
    )

    logger.addHandler(file_handler)

logger.setLevel(logging.INFO)

logger.propagate = False


class SelfHealingState(TypedDict):

    error_log: str

    schema_context: str

    proposed_fix: str

    retry_count: int

    diagnosis: str

    execution_result: str

    healed: bool


def _build_llm() -> ChatOpenAI:

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:

        raise RuntimeError(
            "OPENAI_API_KEY is not set for self-healing agent."
        )

    return ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key, temperature=0)


def diagnose_node(
    state: SelfHealingState,
) -> SelfHealingState:

    logger.info(
        "Diagnose node start | retry_count=%s",
        state["retry_count"],
    )

    llm = _build_llm()

    prompt = (
        "You are a Snowflake troubleshooting expert. "
        "Given this Airflow task log, identify the "
        "root cause and produce a concise diagnosis.\n\n"
        f"Schema Context:\n{state['schema_context']}\n\n"
        f"Error Log:\n{state['error_log']}\n"
    )

    diagnosis = llm.invoke(prompt).content.strip()

    logger.info("Diagnosis: %s", diagnosis)

    state["diagnosis"] = diagnosis

    return state


def patch_node(
    state: SelfHealingState,
) -> SelfHealingState:

    logger.info(
        "Patch node start | retry_count=%s",
        state["retry_count"],
    )

    llm = _build_llm()

    prompt = (
        "Generate a single Snowflake SQL statement "
        "that is safe and idempotent, intended to "
        "heal the diagnosed failure. Return SQL only.\n\n"
        f"Diagnosis:\n{state['diagnosis']}\n\n"
        f"Schema Context:\n{state['schema_context']}\n"
    )

    proposed_fix = (
    llm.invoke(prompt)
    .content
    .replace("```sql", "")
    .replace("```", "")
    .replace("sql\n", "")
    .strip()
)

    logger.info(
        "Proposed SQL fix: %s",
        proposed_fix,
    )

    state["proposed_fix"] = proposed_fix

    return state


def execute_node(
    state: SelfHealingState,
) -> SelfHealingState:

    logger.info(
        "Execute node start | retry_count=%s",
        state["retry_count"],
    )

    tools = SnowflakeMCPTools()

    result = tools.execute_sql(
        state["proposed_fix"]
    )

    state["execution_result"] = str(result)

    state["retry_count"] += 1

    state["healed"] = bool(
        result.get("success")
    )

    if state["healed"]:

        logger.info(
            "SQL fix executed successfully."
        )

    else:

        logger.error(
            "SQL fix failed: %s",
            result,
        )

    return state


def route_after_execute(
    state: SelfHealingState,
) -> Literal["done", "retry"]:

    if state["healed"]:
        return "done"

    if state["retry_count"] >= 3:
        return "done"

    return "retry"


def build_graph():

    graph = StateGraph(SelfHealingState)

    graph.add_node(
        "diagnose",
        diagnose_node,
    )

    graph.add_node(
        "patch",
        patch_node,
    )

    graph.add_node(
        "execute",
        execute_node,
    )

    graph.set_entry_point(
        "diagnose"
    )

    graph.add_edge(
        "diagnose",
        "patch",
    )

    graph.add_edge(
        "patch",
        "execute",
    )

    graph.add_conditional_edges(
        "execute",
        route_after_execute,
        {
            "done": END,
            "retry": "diagnose",
        },
    )

    return graph.compile()


def run_self_healing_agent(
    error_log: str,
    schema_context: str = "",
) -> dict:

    app = build_graph()

    init_state: SelfHealingState = {

        "error_log": error_log,

        "schema_context": schema_context,

        "proposed_fix": "",

        "retry_count": 0,

        "diagnosis": "",

        "execution_result": "",

        "healed": False,
    }

    final_state = app.invoke(init_state)

    logger.info(
        "Self-healing completed | healed=%s | retries=%s",
        final_state["healed"],
        final_state["retry_count"],
    )

    return final_state