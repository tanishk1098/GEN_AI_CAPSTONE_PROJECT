

# # mcp/snowflake_mcp.py

# import pandas as pd

# from database.snowflake_connection import (
#     create_snowflake_connection
# )


# def discover_tables():

#     conn = create_snowflake_connection()

#     query = "SHOW TABLES"

#     df = pd.read_sql(query, conn)

#     conn.close()

#     return df


# def extract_schema(table_name):

#     conn = create_snowflake_connection()

#     query = f"DESCRIBE TABLE {table_name}"

#     schema_df = pd.read_sql(query, conn)

#     conn.close()

#     return schema_df


# def generate_sample_dataset(
#     table_name,
#     sample_size=1000
# ):

#     conn = create_snowflake_connection()

#     query = f'''
#     SELECT *
#     FROM {table_name}
#     SAMPLE ({sample_size} ROWS)
#     '''

#     df = pd.read_sql(query, conn)

#     conn.close()

#     return df


# mcp/snowflake_mcp.py

import pandas as pd

from database.snowflake_connection import (
    create_snowflake_connection
)

# =========================================
# DISCOVER BUSINESS TABLES
# =========================================

def discover_tables():

    conn = create_snowflake_connection()

    query = """
    SHOW TABLES
    """

    df = pd.read_sql(query, conn)

    # =====================================
    # KEEP ONLY REQUIRED BUSINESS TABLES
    # =====================================

    allowed_tables = [

        "RAW_SALES_BRONZE",

        "FACT_SALES_SILVER",

        "DIM_SALES_SUMMARY_GOLD"
    ]

    df = df[
        df["name"].isin(allowed_tables)
    ]

    conn.close()

    return df


# =========================================
# EXTRACT TABLE SCHEMA
# =========================================

def extract_schema(table_name):

    conn = create_snowflake_connection()

    query = f"""
    DESCRIBE TABLE {table_name}
    """

    schema_df = pd.read_sql(query, conn)

    conn.close()

    return schema_df


# =========================================
# GENERATE SAMPLE DATASET
# =========================================

def generate_sample_dataset(
    table_name,
    sample_size=1000
):

    conn = create_snowflake_connection()

    query = f"""
    SELECT *
    FROM {table_name}
    SAMPLE ({sample_size} ROWS)
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df