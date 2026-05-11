"""Local MCP-style tools for Snowflake repair operations."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import snowflake.connector


@dataclass
class SnowflakeMCPTools:
    """Thin local tool wrapper used by the self-healing graph."""

    account: str | None = None
    user: str | None = None
    password: str | None = None
    warehouse: str | None = None
    database: str | None = None
    schema: str | None = None
    role: str | None = None

    def __post_init__(self) -> None:
        self.account = self.account or os.getenv("SNOWFLAKE_ACCOUNT")
        self.user = self.user or os.getenv("SNOWFLAKE_USER")
        self.password = self.password or os.getenv("SNOWFLAKE_PASSWORD")
        self.warehouse = self.warehouse or os.getenv("SNOWFLAKE_WAREHOUSE")
        self.database = self.database or os.getenv("SNOWFLAKE_DATABASE")
        self.schema = self.schema or os.getenv("SNOWFLAKE_SCHEMA")
        self.role = self.role or os.getenv("SNOWFLAKE_ROLE")

    def execute_sql(self, query: str) -> dict[str, Any]:
        """Execute DDL/DML patch SQL against Snowflake."""
        if not query or not query.strip():
            raise ValueError("execute_sql requires a non-empty query.")

        conn = snowflake.connector.connect(
            account=self.account,
            user=self.user,
            password=self.password,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.schema,
            role=self.role,
        )
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rowcount = cursor.rowcount
            conn.commit()
            return {"success": True, "rowcount": rowcount, "query": query}
        except Exception as exc:
            conn.rollback()
            return {"success": False, "error": str(exc), "query": query}
        finally:
            conn.close()

