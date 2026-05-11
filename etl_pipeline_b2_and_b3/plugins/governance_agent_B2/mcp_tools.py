"""Snowflake MCP tools."""

from __future__ import annotations

import os
from typing import Any

import snowflake.connector


class SnowflakeMCPTools:
    def __init__(self):
        self.conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
            role=os.getenv("SNOWFLAKE_ROLE"),
        )

    def execute_sql(self, query: str) -> dict[str, Any]:
        try:
            cursor = self.conn.cursor()

            cursor.execute(query)

            try:
                rows = cursor.fetchall()
            except Exception:
                rows = []

            return {
                "success": True,
                "rows": rows,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }