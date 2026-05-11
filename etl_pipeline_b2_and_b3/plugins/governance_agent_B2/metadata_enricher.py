"""Metadata enrichment."""

from __future__ import annotations


def generate_tags(
    pii_columns: list[str],
    target_tables: list[str],
) -> list[str]:

    tags = ["Governed"]

    if pii_columns:
        tags.append("PII")

    for table in target_tables:
        upper_table = table.upper()

        if "BRONZE" in upper_table:
            tags.append("Bronze")

        elif "SILVER" in upper_table:
            tags.append("Silver")

        elif "GOLD" in upper_table:
            tags.append("Gold")

    return list(set(tags))