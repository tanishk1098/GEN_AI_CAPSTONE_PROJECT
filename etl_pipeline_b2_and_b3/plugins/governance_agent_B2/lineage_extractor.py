"""Extract SQL lineage."""

from __future__ import annotations

import sqlglot
from sqlglot import expressions as exp

from governance_agent_B2.models import (
    LineageResult,
)


def extract_lineage(sql_text: str) -> LineageResult:
    parsed = sqlglot.parse_one(
        sql_text,
        read="snowflake",
    )

    source_tables = []

    target_tables = []

    column_mapping = {}

    # Extract source tables
    for table in parsed.find_all(exp.Table):
        source_tables.append(str(table))

    # Handle COPY INTO
    copy_node = parsed.find(exp.Copy)

    if copy_node:

        schema = copy_node.this

        # Extract target table + columns
        if isinstance(schema, exp.Schema):

            # Target table
            if schema.this:
                target_tables.append(str(schema.this))

            # Column extraction
            for column in schema.expressions:
                column_mapping[
                    str(column)
                ] = str(column)

    # Handle INSERT INTO
    insert_node = parsed.find(exp.Insert)

    if insert_node:
        target_tables.append(str(insert_node.this))

    # Handle SELECT projections
    select_node = parsed.find(exp.Select)

    if select_node:
        for projection in select_node.expressions:
            column_mapping[
                str(projection)
            ] = str(projection)

    return {
        "source_tables": list(set(source_tables)),
        "target_tables": list(set(target_tables)),
        "column_mapping": column_mapping,
    }