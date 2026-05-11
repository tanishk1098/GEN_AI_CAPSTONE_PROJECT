from dotenv import load_dotenv
import os
import snowflake.connector

# =====================================
# LOAD ENV VARIABLES
# =====================================

load_dotenv()

# =====================================
# CREATE CONNECTION
# =====================================

try:

    conn = snowflake.connector.connect(

        user=os.getenv("SNOWFLAKE_USER"),

        password=os.getenv("SNOWFLAKE_PASSWORD"),

        account=os.getenv("SNOWFLAKE_ACCOUNT"),

        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE")
    )

    print("SUCCESS: Connected to Snowflake")

    # =================================
    # TEST QUERY
    # =================================

    cursor = conn.cursor()

    cursor.execute("SELECT CURRENT_VERSION()")

    version = cursor.fetchone()

    print("Snowflake Version:", version)

    cursor.close()

    conn.close()

except Exception as e:

    print("ERROR:", e)