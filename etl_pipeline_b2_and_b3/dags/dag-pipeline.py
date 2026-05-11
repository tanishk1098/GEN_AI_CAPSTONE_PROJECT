# from datetime import datetime

# from airflow import DAG
# from airflow.providers.common.sql.operators.sql import (
#     SQLExecuteQueryOperator,
# )

# from self_healing_agent_B3.callbacks import (
#     self_healing_failure_callback,
# )

# default_args = {
#     "owner": "data_engineering",
#     "start_date": datetime(2026, 5, 1),
#     "on_failure_callback": self_healing_failure_callback,
# }

# with DAG(
#     dag_id="snowflake_medallion_etl_modular",
#     default_args=default_args,
#     schedule="@daily",
#     catchup=False,
# ) as dag:

#     load_bronze = SQLExecuteQueryOperator(
#         task_id="load_to_bronze",
#         conn_id="snowflake_default",
#         sql="""
#         EXECUTE IMMEDIATE FROM
#         @sql_scripts_stage/01_load_bronze.sql;
#         """,
#     )

#     transform_silver = SQLExecuteQueryOperator(
#         task_id="transform_to_silver",
#         conn_id="snowflake_default",
#         sql="""
#         EXECUTE IMMEDIATE FROM
#         @sql_scripts_stage/02_transform_silver.sql;
#         """,
#     )

#     calculate_gold = SQLExecuteQueryOperator(
#         task_id="calculate_gold_kpis",
#         conn_id="snowflake_default",
#         sql="""
#         EXECUTE IMMEDIATE FROM
#         @sql_scripts_stage/03_calculate_gold.sql;
#         """,
#     )

#     load_bronze >> transform_silver >> calculate_gold

from datetime import datetime

from airflow import DAG

from airflow.operators.python import PythonOperator

from airflow.providers.common.sql.operators.sql import (
    SQLExecuteQueryOperator,
)

from governance_agent_B2.governance_agent import (
    run_governance_checks,
)

from self_healing_agent_B3.callbacks import (
    self_healing_failure_callback,
)


default_args = {
    "owner": "data_engineering",
    "start_date": datetime(2026, 5, 1),
    "on_failure_callback": self_healing_failure_callback,
}


with DAG(
    "snowflake_medallion_etl_modular",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:

    validate_governance = PythonOperator(
        task_id="validate_governance",
        python_callable=run_governance_checks,
    )

    load_bronze = SQLExecuteQueryOperator(
        task_id="load_to_bronze",
        conn_id="snowflake_default",
        sql="EXECUTE IMMEDIATE FROM @sql_scripts_stage/01_load_bronze.sql;",
    )

    transform_silver = SQLExecuteQueryOperator(
        task_id="transform_to_silver",
        conn_id="snowflake_default",
        sql="EXECUTE IMMEDIATE FROM @sql_scripts_stage/02_transform_silver.sql;",
    )

    calculate_gold = SQLExecuteQueryOperator(
        task_id="calculate_gold_kpis",
        conn_id="snowflake_default",
        sql="EXECUTE IMMEDIATE FROM @sql_scripts_stage/03_calculate_gold.sql;",
    )

    (
        validate_governance
        >> load_bronze
        >> transform_silver
        >> calculate_gold
    )