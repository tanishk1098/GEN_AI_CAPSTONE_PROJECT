"""Catalogue persistence layer."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from governance_agent_B2.models import GovernanceResult


logger = logging.getLogger("catalog_store")


CATALOG_PATH = "/opt/airflow/logs/governance_catalog.json"


def persist_metadata(result: GovernanceResult) -> None:
    path = Path(CATALOG_PATH)

    existing = []

    if path.exists():
        existing = json.loads(path.read_text())

    existing.append(result)

    path.write_text(json.dumps(existing, indent=2))

    logger.info("Governance metadata persisted")