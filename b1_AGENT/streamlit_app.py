# # =========================================
# # PAGE CONFIG
# # =========================================

# import streamlit as st
# import pandas as pd
# import traceback
# import logging
# import json
# #THESE IMPORTS ARE NOT BEING USED NOW AS STREAMLIT NOWNHANDKLES ONLY UI RESPNSIIBLITY , AND LANGGRAPH HANDLES THEORCHESTRATION , BUT THEY ARE LEFT HERE FOR FUTURE EXTENSIONS
# # from agents.profiler import profile_data
# # from agents.rule_generator import generate_rules
# # from agents.validator import validate_data
# # from agents.healer import self_heal

# from agents.semantic_healer import infer_category
# from workflow.agent_graph import workflow
# from agents.insights_generator import generate_business_insights
# from mcp.snowflake_mcp import (
#     discover_tables,
#     generate_sample_dataset
# )
# # =========================================
# # LOGGING CONFIG
# # =========================================

# logging.basicConfig(

#     filename="logs/pipeline.log",

#     level=logging.INFO,

#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# st.set_page_config(
#     page_title="AI Ingestion Quality Agent",
#     layout="wide"
# )

# # =========================================
# # TITLE SECTION
# # =========================================

# st.title("AI-Powered Autonomous Data Engineering Agent")

# st.markdown("""
# ## Bronze → Silver → Gold Autonomous Pipeline

# Transform raw datasets into production-ready analytics using AI agents.

# ### What this system does

# ✅ Intelligent Data Profiling  
# ✅ Automated Rule Generation  
# ✅ AI-Powered Validation  
# ✅ Autonomous Self-Healing  
# ✅ Semantic Data Repair  
# ✅ Silver Layer Dataset Creation  
# ✅ Gold Layer KPI & Business Analytics  
# ✅ Dynamic Visualizations  
# ✅ LangGraph Multi-Agent Workflow  

# ---

# ### AI Agents Inside the Pipeline

# | Agent | Responsibility |
# |---|---|
# | Profiler Agent | Understands dataset structure |
# | Rule Generator Agent | Creates validation rules |
# | Validator Agent | Detects quality issues |
# | Self-Healing Agent | Repairs corrupted data |
# | Semantic AI Agent | Infers missing meanings |
# | Analytics Agent | Builds KPIs & insights |
# """)

# # =========================================
# # SIDEBAR
# # =========================================

# with st.sidebar:

#     st.title("AI Pipeline Control")

#     st.success("Bronze → Silver → Gold")
    
#     logging.info(
#         "Autonomous pipeline execution completed successfully"
#     )

#     st.markdown("---")

#     run_pipeline = st.button(
#         "Run Autonomous Pipeline",
#         use_container_width=True
#     )

#     st.markdown("---")

#     st.markdown("""
#     ### Pipeline Workflow

#     ```text
#     Discover Snowflake Tables
#             ↓
#     Profiling Agent
#             ↓
#     Rule Generator
#             ↓
#     Validation Agent
#             ↓
#     Self-Healing Agent
#             ↓
#     Semantic AI Agent
#             ↓
#     KPI & Analytics Engine
#             ↓
#     Gold Layer Dashboard
#     ```
#     """)

#     st.markdown("---")

#     st.info(
#         "Select Snowflake tables and click 'Run Autonomous Pipeline'."
#     )

# # =========================================
# # FILE UPLOADER
# # =========================================

# # uploaded_files = st.file_uploader(
# #     "Upload CSV Files",
# #     type=["csv"],
# #     accept_multiple_files=True
# # )

# # =========================================
# # SNOWFLAKE TABLE DISCOVERY
# # =========================================

# available_tables_df = discover_tables()

# available_tables = list(
#     available_tables_df["name"]
# )

# selected_tables = st.multiselect(
#     "Select Snowflake Tables",
#     available_tables
# )
# # =========================================
# # TABS
# # =========================================

# bronze_tab, silver_tab, gold_tab = st.tabs(
#     ["Bronze Layer", "Silver Layer", "Gold Layer"]
# )

# # =========================================
# # MAIN PIPELINE
# # =========================================

# if selected_tables and run_pipeline:

#     processed_data = {}

#     validation_summary = []

#     total_errors = 0

#     with st.spinner(
#         "Running autonomous AI pipeline..."
#     ):

#         # =====================================
#         # PROCESS EACH FILE
#         # =====================================

#         for table_name in selected_tables:

#             dataset_name = table_name
            
#             semantic_preview = None
            
#             lineage = {
#                 "source": {
#                     "database": "SNOWFLAKE",
#                     "table": dataset_name,
#                     "layer": "BRONZE"
#                 },
#                 "target": {
#                      "layer": "SILVER"
#                 },
#                 "steps": []
# }

#             try:

#                 # =================================
#                 # LOAD DATASET
#                 # =================================

#                 df = generate_sample_dataset(
#                     table_name,
#                     sample_size=1000
#                 )
                
#                 logging.info(
#                     f"{dataset_name} loaded successfully"
#                 )

#                 # =================================
#                 # SEMANTIC AI PREVIEW
#                 # =================================

#                 if "product_category_name" in df.columns:

#                     semantic_preview = df.head(5).copy()

#                     semantic_preview[
#                         "ai_generated_category"
#                     ] = (
#                         semantic_preview[
#                             "product_category_name"
#                         ]
#                         .astype(str)
#                         .apply(infer_category)
#                     )

#                 # =================================
#                 # SAVE BRONZE
#                 # =================================

#                 df.to_csv(
#                     f"outputs/bronze/{dataset_name}",
#                     index=False
#                 )
#                 sql_query = f'''
#                 CREATE TABLE clean_{dataset_name} AS
#                 SELECT *
#                 FROM {dataset_name}
#                 '''
#                 # =================================
#                 # RUN AGENTIC WORKFLOW
#                 # =================================

#                 result = workflow.invoke({
#                     "table_name": table_name,
#                     "df": df,
#                     "sql_query": sql_query})

#                 profile = result["profile"]
                
#                 lineage["steps"].append(
#                     "Profiler Agent Completed"
#                 )

#                 rules = result["rules"]

#                 errors = result["errors"]
                
#                 lineage["steps"].append(
#                     "Validation Agent Completed"
#                 )

#                 clean_df = result.get(
#                 "clean_df",
#                  df
#                 )
#                 governance_metadata = result[
#                      "governance_metadata"
#                 ]
                
#                 lineage["steps"].append(
#                     "Self-Healing Agent Completed"
#                 )
                
#                 logging.info(
#                     f"{dataset_name} self-healing completed"
#                 )

#                 error_count = len(errors)
                
#                 logging.info(
#                     f"{dataset_name} validation completed with {error_count} issues"
#                 )

#                 total_errors += error_count

#                 # =================================
#                 # SAVE SILVER
#                 # =================================

#                 clean_df.to_csv(
#                     f"outputs/silver/clean_{dataset_name}",
#                     index=False
#                 )

#                 # =================================
#                 # STORE RESULTS
#                 # =================================

#                 processed_data[dataset_name] = {

#                     "raw_df": df,

#                     "clean_df": clean_df,

#                     "profile": profile,

#                     "rules": rules,

#                     "errors": errors,

#                     "semantic_preview": semantic_preview,

#                     "governance_metadata": governance_metadata
#                 }
                
#                 with open(
#                     f"metadata/{dataset_name}_lineage.json",
#                     "w"
#                 ) as f:

#                     json.dump(
#                         lineage,
#                         f,
#                         indent=4
#                     )
#                 with open(
#                     f"metadata/{dataset_name}_governance.json",
#                     "w"
#                 ) as f:
#                     json.dump(
#                         governance_metadata,
#                         f,
#                         indent=4
#                     )
#                 # =================================
#                 # VALIDATION SUMMARY
#                 # =================================
#                 validation_summary.append({

#                     "Dataset": dataset_name,

#                     "Rows": df.shape[0],

#                     "Columns": df.shape[1],

#                     "Issues Found": error_count,

#                     "Status": "Cleaned Successfully"
#                 })

#             except Exception:

#                 st.error(
#                     f"Error processing {dataset_name}"
#                 )

#                 st.code(
#                     traceback.format_exc()
#                 )

#     # =========================================
#     # BRONZE LAYER
#     # =========================================

#     with bronze_tab:

#         st.header("Bronze Layer - Raw Datasets")

#         st.markdown("""
#         Raw uploaded datasets before validation and cleaning.
#         """)

#         for dataset_name, data in processed_data.items():

#             df = data["raw_df"]

#             st.subheader(dataset_name)

#             col1, col2 = st.columns(2)

#             with col1:
#                 st.metric(
#                     "Rows",
#                     df.shape[0]
#                 )

#             with col2:
#                 st.metric(
#                     "Columns",
#                     df.shape[1]
#                 )

#             st.dataframe(df.head())

#             st.divider()

#     # =========================================
#     # SILVER LAYER
#     # =========================================

#     with silver_tab:

#         st.header("Silver Layer - Cleaned Datasets")

#         st.subheader("Validation Summary")

#         summary_df = pd.DataFrame(
#             validation_summary
#         )

#         st.dataframe(summary_df)

#         st.divider()

#         for dataset_name, data in processed_data.items():

#             clean_df = data["clean_df"]

#             errors = data["errors"]

#             st.subheader(dataset_name)

#             st.success(
#                 "Dataset cleaned successfully"
#             )

#             st.write(
#                 f"Validation Issues Found: {len(errors)}"
#             )

#             if len(errors) > 0:

#                 error_df = pd.DataFrame(errors)

#                 st.dataframe(error_df)

#             st.dataframe(clean_df.head())

#             csv = clean_df.to_csv(index=False)

#             st.download_button(

#                 label=f"Download Cleaned {dataset_name}",

#                 data=csv,

#                 file_name=f"clean_{dataset_name}",

#                 mime="text/csv"
#             )

#             st.divider()

#     # =========================================
#     # GOLD LAYER
#     # =========================================

#     with gold_tab:

#         st.header("Gold Layer - Analytics & KPIs")

#         st.markdown("""
#         ### Executive Analytics Dashboard

#         Business-ready KPIs generated automatically from cleaned datasets.
#         """)

#         total_datasets = len(processed_data)

#         total_rows = sum(
#             data["clean_df"].shape[0]
#             for data in processed_data.values()
#         )

#         # =====================================
#         # KPI SECTION
#         # =====================================

#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.metric(
#                 "Datasets Processed",
#                 total_datasets
#             )

#         with col2:
#             st.metric(
#                 "Total Rows Processed",
#                 total_rows
#             )

#         with col3:
#             st.metric(
#                 "Validation Issues Fixed",
#                 total_errors
#             )

#         st.divider()

#         # =====================================
#         # VALIDATION SUMMARY
#         # =====================================

#         st.markdown("## Dataset Processing Overview")

#         st.dataframe(
#             pd.DataFrame(validation_summary)
#         )

#         st.divider()

#         # =====================================
#         # CUSTOMER ANALYTICS
#         # =====================================

#         if "olist_customers_dataset.csv" in processed_data:

#             customer_df = processed_data[
#                 "olist_customers_dataset.csv"
#             ]["clean_df"]

#             if "customer_state" in customer_df.columns:

#                 st.markdown("## Top Customer States")

#                 state_mapping = {

#                     "SP": "São Paulo",

#                     "RJ": "Rio de Janeiro",

#                     "MG": "Minas Gerais",

#                     "BA": "Bahia",

#                     "PR": "Paraná",

#                     "RS": "Rio Grande do Sul",

#                     "SC": "Santa Catarina",

#                     "GO": "Goiás",

#                     "PE": "Pernambuco",

#                     "CE": "Ceará"
#                 }

#                 customer_df[
#                     "state_full_name"
#                 ] = (
#                     customer_df[
#                         "customer_state"
#                     ]
#                     .map(state_mapping)
#                     .fillna(
#                         customer_df[
#                             "customer_state"
#                         ]
#                     )
#                 )

#                 state_counts = (
#                     customer_df[
#                         "state_full_name"
#                     ]
#                     .value_counts()
#                     .head(10)
#                 )

#                 st.bar_chart(state_counts)

#         # =====================================
#         # TOP CITIES
#         # =====================================

#         if "olist_customers_dataset.csv" in processed_data:

#             customer_df = processed_data[
#                 "olist_customers_dataset.csv"
#             ]["clean_df"]

#             if "customer_city" in customer_df.columns:

#                 st.markdown("## Top Customer Cities")

#                 city_counts = (
#                     customer_df["customer_city"]
#                     .astype(str)
#                     .str.title()
#                     .value_counts()
#                     .head(10)
#                 )

#                 st.bar_chart(city_counts)

#         # =====================================
#         # PAYMENT ANALYTICS
#         # =====================================

#         if "olist_order_payments_dataset.csv" in processed_data:

#             payment_df = processed_data[
#                 "olist_order_payments_dataset.csv"
#             ]["clean_df"]

#             if (
#                 "payment_type" in payment_df.columns
#                 and
#                 "payment_value" in payment_df.columns
#             ):

#                 st.markdown(
#                     "## Revenue by Payment Type"
#                 )

#                 revenue_by_payment = (
#                     payment_df.groupby(
#                         "payment_type"
#                     )["payment_value"]
#                     .sum()
#                     .sort_values(
#                         ascending=False
#                     )
#                 )

#                 st.bar_chart(
#                     revenue_by_payment
#                 )

#                 avg_payment = round(
#                     payment_df[
#                         "payment_value"
#                     ].mean(),
#                     2
#                 )

#                 st.metric(
#                     "Average Payment Value",
#                     f"${avg_payment}"
#                 )

#         # =====================================
#         # MERGED GOLD ANALYTICS
#         # =====================================

#         if (
#             "olist_orders_dataset.csv"
#             in processed_data
#             and
#             "olist_order_payments_dataset.csv"
#             in processed_data
#         ):

#             orders_df = processed_data[
#                 "olist_orders_dataset.csv"
#             ]["clean_df"]

#             payments_df = processed_data[
#                 "olist_order_payments_dataset.csv"
#             ]["clean_df"]

#             merged_df = pd.merge(

#                 orders_df,

#                 payments_df,

#                 on="order_id",

#                 how="inner"
#             )

#             st.divider()

#             st.markdown(
#                 "## Merged Gold Layer Analytics"
#             )

#             total_revenue = round(
#                 merged_df[
#                     "payment_value"
#                 ].sum(),
#                 2
#             )

#             avg_order_value = round(
#                 merged_df[
#                     "payment_value"
#                 ].mean(),
#                 2
#             )

#             unique_orders = (
#                 merged_df[
#                     "order_id"
#                 ]
#                 .nunique()
#             )

#             col1, col2, col3 = st.columns(3)

#             with col1:
#                 st.metric(
#                     "Total Revenue",
#                     f"${total_revenue}"
#                 )

#             with col2:
#                 st.metric(
#                     "Average Order Value",
#                     f"${avg_order_value}"
#                 )

#             with col3:
#                 st.metric(
#                     "Unique Orders",
#                     unique_orders
#                 )

#             if "payment_type" in merged_df.columns:

#                 st.markdown(
#                     "## Payment Type Distribution"
#                 )

#                 payment_counts = (
#                     merged_df[
#                         "payment_type"
#                     ]
#                     .value_counts()
#                 )

#                 st.bar_chart(payment_counts)

#             st.markdown(
#                 "## Merged Dataset Preview"
#             )

#             st.dataframe(
#                 merged_df.head()
#             )

#         # =====================================
#         # GOVERNANCE METADATA
#         # =====================================

#         st.divider()

#         st.markdown(
#             "## Governance Metadata"
#         )

#         for dataset_name, data in processed_data.items():

#             st.subheader(dataset_name)

#             governance_file = (
#                 f"metadata/{dataset_name}_governance.json"
#             )

#             try:

#                 with open(governance_file, "r") as f:

#                     governance_data = json.load(f)

#                 st.json(governance_data)

#             except:

#                 st.warning(
#                     "No governance metadata found."
#                 )   
  
#         # =====================================
#         # AI BUSINESS INSIGHTS
#         # =====================================

#         summary = {

#             "total_datasets": total_datasets,

#             "total_rows": total_rows,

#             "total_errors_fixed": total_errors
#         }

#         insights = generate_business_insights(
#             summary
#         )

#         st.divider()

#         st.markdown(
#             "## AI Generated Business Insights"
#         )

#         st.write(insights)

#         # =====================================
#         # AI SEMANTIC PREVIEW
#         # =====================================

#         for dataset_name, data in processed_data.items():

#             semantic_preview = data[
#                 "semantic_preview"
#             ]

#             if semantic_preview is not None:

#                 st.markdown(
#                     f"## Semantic AI Preview - {dataset_name}"
#                 )

#                 st.dataframe(
#                     semantic_preview
#                 )

#         # =====================================
#         # GENERIC VISUALIZATIONS
#         # =====================================

#         st.divider()

#         st.markdown(
#             "## Automatic Dataset Visualizations"
#         )

#         for dataset_name, data in processed_data.items():

#             df = data["clean_df"]

#             st.subheader(dataset_name)

#             # ================================
#             # CATEGORICAL CHARTS
#             # ================================

#             categorical_cols = df.select_dtypes(
#                 include=["object"]
#             ).columns

#             for col in categorical_cols[:2]:

#                 try:

#                     st.write(
#                         f"Top values in {col}"
#                     )

#                     value_counts = (
#                         df[col]
#                         .astype(str)
#                         .value_counts()
#                         .head(10)
#                     )

#                     st.bar_chart(value_counts)

#                 except:
#                     pass

#             # ================================
#             # NUMERIC CHARTS
#             # ================================

#             numeric_cols = df.select_dtypes(
#                 include=["int64", "float64"]
#             ).columns

#             for col in numeric_cols[:2]:

#                 try:

#                     st.write(
#                         f"Distribution of {col}"
#                     )

#                     st.line_chart(
#                         df[col].head(50)
#                     )

#                 except:
#                     pass

#             st.divider()

#         st.success(
#             "All datasets successfully processed through Bronze → Silver → Gold pipeline"
#         )

# # =========================================
# # NO FILES
# # =========================================

# else:

#     st.info(
#         "Upload one or more CSV datasets and click 'Run Autonomous Pipeline'."
#     )

# # =========================================
# # FOOTER
# # =========================================

# # st.markdown("---")

# st.caption(
#     "Built with Streamlit • Pandas • LangGraph • Autonomous AI Agents"
# )

# available_tables_df = discover_tables()
# st.write(available_tables_df)





# =========================================
# PAGE CONFIG
# =========================================

import streamlit as st
import pandas as pd
import traceback
import logging

# THESE IMPORTS ARE NOT BEING USED NOW AS STREAMLIT NOW HANDLES ONLY UI RESPONSIBILITY,
# AND LANGGRAPH HANDLES THE ORCHESTRATION, BUT THEY ARE LEFT HERE FOR FUTURE EXTENSIONS

# from agents.profiler import profile_data
# from agents.rule_generator import generate_rules
# from agents.validator import validate_data
# from agents.healer import self_heal

from agents.semantic_healer import infer_category
from workflow.agent_graph import workflow
from agents.insights_generator import generate_business_insights
from mcp.snowflake_mcp import (
    discover_tables,
    generate_sample_dataset
)

# =========================================
# LOGGING CONFIG
# =========================================

logging.basicConfig(

    filename="logs/pipeline.log",

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"

)

st.set_page_config(
    page_title="AI Ingestion Quality Agent",
    layout="wide"
)

# =========================================
# TITLE SECTION
# =========================================

st.title("AI-Powered Autonomous Data Engineering Agent")

st.markdown("""

## Bronze → Silver → Gold Autonomous Pipeline

Transform raw datasets into production-ready analytics using AI agents.

### What this system does

✅ Intelligent Data Profiling  
✅ Automated Rule Generation  
✅ AI-Powered Validation  
✅ Autonomous Self-Healing  
✅ Semantic Data Repair  
✅ Silver Layer Dataset Creation  
✅ Gold Layer KPI & Business Analytics  
✅ Dynamic Visualizations  
✅ LangGraph Multi-Agent Workflow  

---

### AI Agents Inside the Pipeline

| Agent | Responsibility |
|---|---|
| Profiler Agent | Understands dataset structure |
| Rule Generator Agent | Creates validation rules |
| Validator Agent | Detects quality issues |
| Self-Healing Agent | Repairs corrupted data |
| Semantic AI Agent | Infers missing meanings |
| Analytics Agent | Builds KPIs & insights |

""")

# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.title("AI Pipeline Control")

    st.success("Bronze → Silver → Gold")

    logging.info(
        "Autonomous pipeline execution completed successfully"
    )

    st.markdown("---")

    run_pipeline = st.button(
        "Run Autonomous Pipeline",
        use_container_width=True
    )

    st.markdown("---")

    st.markdown("""
    ### Pipeline Workflow

    ```text
    Discover Snowflake Tables
            ↓
    Profiling Agent
            ↓
    Rule Generator
            ↓
    Validation Agent
            ↓
    Self-Healing Agent
            ↓
    Semantic AI Agent
            ↓
    KPI & Analytics Engine
            ↓
    Gold Layer Dashboard
    ```
    """)

    st.markdown("---")

    st.info(
        "Select Snowflake tables and click 'Run Autonomous Pipeline'."
    )

# =========================================
# SNOWFLAKE TABLE DISCOVERY
# =========================================

available_tables_df = discover_tables()

available_tables = list(
    available_tables_df["name"]
)

selected_tables = st.multiselect(
    "Select Snowflake Tables",
    available_tables
)

# =========================================
# TABS
# =========================================

bronze_tab, silver_tab, gold_tab = st.tabs(
    ["Bronze Layer", "Silver Layer", "Gold Layer"]
)

# =========================================
# MAIN PIPELINE
# =========================================

if selected_tables and run_pipeline:

    processed_data = {}

    validation_summary = []

    total_errors = 0

    with st.spinner(
        "Running autonomous AI pipeline..."
    ):

        # =====================================
        # PROCESS EACH TABLE
        # =====================================

        for table_name in selected_tables:

            dataset_name = table_name

            semantic_preview = None

            try:

                # =================================
                # LOAD DATASET
                # =================================

                df = generate_sample_dataset(
                    table_name,
                    sample_size=1000
                )

                logging.info(
                    f"{dataset_name} loaded successfully"
                )

                # =================================
                # SEMANTIC AI PREVIEW
                # =================================

                if "product_category_name" in df.columns:

                    semantic_preview = df.head(5).copy()

                    semantic_preview[
                        "ai_generated_category"
                    ] = (
                        semantic_preview[
                            "product_category_name"
                        ]
                        .astype(str)
                        .apply(infer_category)
                    )

                # =================================
                # SAVE BRONZE
                # =================================

                df.to_csv(
                    f"outputs/bronze/{dataset_name}",
                    index=False
                )

                # =================================
                # RUN AGENTIC WORKFLOW
                # =================================

                result = workflow.invoke({
                    "table_name": table_name,
                    "df": df
                })

                profile = result["profile"]

                rules = result["rules"]

                errors = result["errors"]

                clean_df = result.get(
                    "clean_df",
                    df
                )

                logging.info(
                    f"{dataset_name} self-healing completed"
                )

                error_count = len(errors)

                logging.info(
                    f"{dataset_name} validation completed with {error_count} issues"
                )

                total_errors += error_count

                # =================================
                # SAVE SILVER
                # =================================

                clean_df.to_csv(
                    f"outputs/silver/clean_{dataset_name}",
                    index=False
                )

                # =================================
                # STORE RESULTS
                # =================================

                processed_data[dataset_name] = {

                    "raw_df": df,

                    "clean_df": clean_df,

                    "profile": profile,

                    "rules": rules,

                    "errors": errors,

                    "semantic_preview": semantic_preview
                }

                # =================================
                # VALIDATION SUMMARY
                # =================================

                validation_summary.append({

                    "Dataset": dataset_name,

                    "Rows": df.shape[0],

                    "Columns": df.shape[1],

                    "Issues Found": error_count,

                    "Status": "Cleaned Successfully"
                })

            except Exception:

                st.error(
                    f"Error processing {dataset_name}"
                )

                st.code(
                    traceback.format_exc()
                )

    # =========================================
    # BRONZE LAYER
    # =========================================

    with bronze_tab:

        st.header("Bronze Layer - Raw Datasets")

        st.markdown("""
        Raw uploaded datasets before validation and cleaning.
        """)

        for dataset_name, data in processed_data.items():

            df = data["raw_df"]

            st.subheader(dataset_name)

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Rows",
                    df.shape[0]
                )

            with col2:
                st.metric(
                    "Columns",
                    df.shape[1]
                )

            st.dataframe(df.head())

            st.divider()

    # =========================================
    # SILVER LAYER
    # =========================================

    with silver_tab:

        st.header("Silver Layer - Cleaned Datasets")

        st.subheader("Validation Summary")

        summary_df = pd.DataFrame(
            validation_summary
        )

        st.dataframe(summary_df)

        st.divider()

        for dataset_name, data in processed_data.items():

            clean_df = data["clean_df"]

            errors = data["errors"]

            st.subheader(dataset_name)

            st.success(
                "Dataset cleaned successfully"
            )

            st.write(
                f"Validation Issues Found: {len(errors)}"
            )

            if len(errors) > 0:

                error_df = pd.DataFrame(errors)

                st.dataframe(error_df)

            st.dataframe(clean_df.head())

            csv = clean_df.to_csv(index=False)

            st.download_button(

                label=f"Download Cleaned {dataset_name}",

                data=csv,

                file_name=f"clean_{dataset_name}",

                mime="text/csv"
            )

            st.divider()

    # =========================================
    # GOLD LAYER
    # =========================================

    with gold_tab:

        st.header("Gold Layer - Analytics & KPIs")

        st.markdown("""
        ### Executive Analytics Dashboard

        Business-ready KPIs generated automatically from cleaned datasets.
        """)

        total_datasets = len(processed_data)

        total_rows = sum(
            data["clean_df"].shape[0]
            for data in processed_data.values()
        )

        # =====================================
        # KPI SECTION
        # =====================================

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Datasets Processed",
                total_datasets
            )

        with col2:
            st.metric(
                "Total Rows Processed",
                total_rows
            )

        with col3:
            st.metric(
                "Validation Issues Fixed",
                total_errors
            )

        st.divider()

        # =====================================
        # VALIDATION SUMMARY
        # =====================================

        st.markdown("## Dataset Processing Overview")

        st.dataframe(
            pd.DataFrame(validation_summary)
        )

        st.divider()

        # =====================================
        # AI BUSINESS INSIGHTS
        # =====================================

        summary = {

            "total_datasets": total_datasets,

            "total_rows": total_rows,

            "total_errors_fixed": total_errors
        }

        insights = generate_business_insights(
            summary
        )

        st.divider()

        st.markdown(
            "## AI Generated Business Insights"
        )

        st.write(insights)

        # =====================================
        # AI SEMANTIC PREVIEW
        # =====================================

        for dataset_name, data in processed_data.items():

            semantic_preview = data[
                "semantic_preview"
            ]

            if semantic_preview is not None:

                st.markdown(
                    f"## Semantic AI Preview - {dataset_name}"
                )

                st.dataframe(
                    semantic_preview
                )

        # =====================================
        # GENERIC VISUALIZATIONS
        # =====================================

        st.divider()

        st.markdown(
            "## Automatic Dataset Visualizations"
        )

        for dataset_name, data in processed_data.items():

            df = data["clean_df"]

            st.subheader(dataset_name)

            # ================================
            # CATEGORICAL CHARTS
            # ================================

            categorical_cols = df.select_dtypes(
                include=["object"]
            ).columns

            for col in categorical_cols[:2]:

                try:

                    st.write(
                        f"Top values in {col}"
                    )

                    value_counts = (
                        df[col]
                        .astype(str)
                        .value_counts()
                        .head(10)
                    )

                    st.bar_chart(value_counts)

                except:
                    pass

            # ================================
            # NUMERIC CHARTS
            # ================================

            numeric_cols = df.select_dtypes(
                include=["int64", "float64"]
            ).columns

            for col in numeric_cols[:2]:

                try:

                    st.write(
                        f"Distribution of {col}"
                    )

                    st.line_chart(
                        df[col].head(50)
                    )

                except:
                    pass

            st.divider()

        st.success(
            "All datasets successfully processed through Bronze → Silver → Gold pipeline"
        )

# =========================================
# NO FILES
# =========================================

else:

    st.info(
        "Select one or more Snowflake tables and click 'Run Autonomous Pipeline'."
    )

# =========================================
# FOOTER
# =========================================

st.caption(
    "Built with Streamlit • Pandas • LangGraph • Autonomous AI Agents"
)