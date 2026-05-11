"""Governance validation rules."""

from __future__ import annotations


FORBIDDEN_SQL_KEYWORDS = [
    "DROP",
    "TRUNCATE",
    "DELETE",
]

PII_COLUMNS = [
    "EMAIL",
    "PHONE",
    "AADHAR",
    "SSN",
    "PASSWORD",
]


def validate_sql_safety(sql_text: str) -> None:
    upper_sql = sql_text.upper()

    for keyword in FORBIDDEN_SQL_KEYWORDS:
        if keyword in upper_sql:
            raise ValueError(
                f"Forbidden SQL keyword detected: {keyword}"
            )


def validate_pii_columns(columns: list[str]) -> None:
    upper_columns = [col.upper() for col in columns]

    for pii_col in PII_COLUMNS:
        if pii_col in upper_columns:
            raise ValueError(
                f"PII column detected: {pii_col}"
            )