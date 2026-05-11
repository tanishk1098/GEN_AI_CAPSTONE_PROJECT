"""SQL parsing utilities."""

from __future__ import annotations

import sqlglot


def parse_sql(sql_text: str):
    return sqlglot.parse_one(sql_text)