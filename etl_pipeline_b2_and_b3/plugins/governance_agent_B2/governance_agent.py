

"""B2 Governance + Lineage Agent."""

from __future__ import annotations

import logging
from pathlib import Path

from governance_agent_B2.catalog_store import (
    persist_metadata,
)

from governance_agent_B2.lineage_extractor import (
    extract_lineage,
)

from governance_agent_B2.metadata_enricher import (
    generate_tags,
)

from governance_agent_B2.models import GovernanceResult

from governance_agent_B2.pii_classifier import (
    classify_pii,
)


logger = logging.getLogger("governance_agent_B2")

logger.setLevel(logging.INFO)


SQL_FILES = [
    "/opt/airflow/sql_scripts/01_load_bronze.sql",
    "/opt/airflow/sql_scripts/02_transform_silver.sql",
    "/opt/airflow/sql_scripts/03_calculate_gold.sql",
]


def process_sql_file(sql_file: str) -> GovernanceResult:
    logger.info("Processing SQL file: %s", sql_file)

    sql_text = Path(sql_file).read_text()

    logger.info("STEP 1 - extracting lineage")

    lineage = extract_lineage(sql_text)

    logger.info("STEP 2 - lineage extracted")

    columns = list(lineage["column_mapping"].keys())

    logger.info("STEP 3 - classifying pii")

    pii_columns = classify_pii(columns)

    logger.info("STEP 4 - pii classified")

    logger.info("STEP 5 - generating tags")

    tags = generate_tags(
        pii_columns=pii_columns,
        target_tables=lineage["target_tables"],
    )

    logger.info("STEP 6 - tags generated")

    result: GovernanceResult = {
        "lineage": lineage,
        "pii_columns": pii_columns,
        "tags": tags,
    }

    logger.info("STEP 7 - persisting metadata")

    persist_metadata(result)

    logger.info("STEP 8 - metadata persisted")

    logger.info("Governance result: %s", result)

    return result


def run_governance_checks() -> None:
    logger.info("Starting B2 Governance Agent")

    for sql_file in SQL_FILES:
        process_sql_file(sql_file)

    logger.info("B2 Governance completed successfully")









# """B2 Governance Test."""

# from __future__ import annotations

# import logging

# from plugins.governance_agent_B2.lineage_extractor import (
#     extract_lineage,
# )

# logger = logging.getLogger("governance_agent_B2")

# logger.setLevel(logging.INFO)


# def run_governance_checks() -> None:
#     logger.info("B2 governance started")

#     print("STEP 1 START")

#     sql = """
#     INSERT INTO CUSTOMER_GOLD
#     SELECT customer_id, amount
#     FROM CUSTOMER_RAW
#     """

#     lineage = extract_lineage(sql)

#     print("LINEAGE RESULT:")
#     print(lineage)

#     print("STEP 1 SUCCESS")