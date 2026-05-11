"""Airflow callback handlers for the self-healing agent."""

from __future__ import annotations

from pathlib import Path

from airflow.models.taskinstance import TaskInstance
from airflow.utils.log.logging_mixin import LoggingMixin

from self_healing_agent_B3.agent_graph import (
    run_self_healing_agent,
)

logger = LoggingMixin().log


def _read_last_lines(
    file_path: str,
    num_lines: int = 50,
) -> str:

    path = Path(file_path)

    if not path.exists():

        return (
            f"Log file not found: {file_path}"
        )

    lines = path.read_text(
        encoding="utf-8",
        errors="ignore",
    ).splitlines()

    return "\n".join(
        lines[-num_lines:]
    )


def self_healing_failure_callback(
    context: dict,
) -> None:

    ti = context["ti"]

    dag_id = ti.dag_id

    task_id = ti.task_id

    run_id = ti.run_id

    try_number = ti.try_number

    log_path = getattr(
        ti,
        "log_filepath",
        None,
    )

    if not log_path:

        log_path = (
            f"/opt/airflow/logs/dag_id={dag_id}/"
            f"run_id={run_id}/"
            f"task_id={task_id}/"
            f"attempt={try_number}.log"
        )

    error_log_snippet = _read_last_lines(
        log_path,
        num_lines=50,
    )

    schema_context = (
        f"DAG={dag_id}\n"
        f"TASK={task_id}\n"
        f"RUN_ID={run_id}\n"
        "Warehouse context comes from Snowflake env vars."
    )

    logger.info(
        "Triggering self-healing agent for failed task: %s",
        task_id,
    )

    result = run_self_healing_agent(
        error_log=error_log_snippet,
        schema_context=schema_context,
    )

    if not result.get("healed"):

        logger.error(
            "Self-healing agent failed after max retries: %s",
            result,
        )

        return

    logger.info(
        "Self-healing succeeded. Clearing task instance for retry: %s",
        task_id,
    )

    TaskInstance.clear_task_instances(
        tis=[ti],
        dag=ti.task.dag,
    )