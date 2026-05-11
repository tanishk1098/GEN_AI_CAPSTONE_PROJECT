# agents/schema_agent.py

from mcp.snowflake_mcp import (
    extract_schema
)


def schema_discovery_agent(table_name):

    schema = extract_schema(table_name)

    metadata = {
        "table_name": table_name,
        "columns": list(schema["name"]),
        "data_types": list(schema["type"]),
        "total_columns": len(schema)
    }

    return metadata