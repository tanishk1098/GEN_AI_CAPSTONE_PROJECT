from __future__ import annotations

from typing import TypedDict


class LineageResult(TypedDict):
    source_tables: list[str]
    target_tables: list[str]
    column_mapping: dict[str, str]


class GovernanceResult(TypedDict):
    lineage: LineageResult
    pii_columns: list[str]
    tags: list[str]