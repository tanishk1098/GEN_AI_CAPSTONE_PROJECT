from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.profiler import profile_data
from agents.rule_generator import generate_rules
from agents.validator import validate_data
from agents.healer import self_heal

# =========================================
# STATE
# =========================================

class AgentState(TypedDict):

    df: object

    profile: dict

    rules: str

    errors: list

    clean_df: object

# =========================================
# PROFILER NODE
# =========================================

def profiler_node(state):

    df = state["df"]

    profile = profile_data(df)

    return {
        **state,
        "profile": profile
    }

# =========================================
# RULE GENERATOR NODE
# =========================================

def rules_node(state):

    rules = generate_rules(
        state["profile"]
    )

    return {
        **state,
        "rules": rules
    }

# =========================================
# VALIDATOR NODE
# =========================================

def validator_node(state):

    errors = validate_data(
        state["df"]
    )

    return {
        **state,
        "errors": errors
    }

# =========================================
# HEALER NODE
# =========================================

def healer_node(state):

    clean_df = self_heal(
        state["df"]
    )

    return {
        **state,
        "clean_df": clean_df
    }

# =========================================
# BUILD GRAPH
# =========================================

builder = StateGraph(AgentState)

# NODES
builder.add_node(
    "profiler",
    profiler_node
)

builder.add_node(
    "rules",
    rules_node
)

builder.add_node(
    "validator",
    validator_node
)

builder.add_node(
    "healer",
    healer_node
)

# FLOW
builder.set_entry_point(
    "profiler"
)

builder.add_edge(
    "profiler",
    "rules"
)

builder.add_edge(
    "rules",
    "validator"
)

builder.add_edge(
    "validator",
    "healer"
)

builder.add_edge(
    "healer",
    END
)

# COMPILE
workflow = builder.compile()