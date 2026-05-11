"""PII classification module."""

from __future__ import annotations


PII_KEYWORDS = [
    "EMAIL",
    "PHONE",
    "AADHAR",
    "SSN",
    "PASSWORD",
]


def classify_pii(columns: list[str]) -> list[str]:
    pii_columns = []

    for col in columns:
        upper_col = col.upper()

        for keyword in PII_KEYWORDS:
            if keyword in upper_col:
                pii_columns.append(col)

    return pii_columns