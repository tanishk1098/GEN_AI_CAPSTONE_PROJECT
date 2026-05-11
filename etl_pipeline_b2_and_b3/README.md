````md
# AI-Powered Autonomous Data Engineering Agent

## Bronze → Silver → Gold Autonomous Pipeline

An AI-powered autonomous data engineering platform that profiles, validates, cleans, repairs, and transforms raw datasets into analytics-ready business intelligence dashboards using a multi-agent workflow powered by LangGraph.

---

# Project Overview

This project simulates a modern enterprise-grade Data Engineering pipeline using autonomous AI agents.

The system automatically:

- Ingests raw CSV datasets
- Profiles data structures
- Generates validation rules
- Detects data quality issues
- Applies autonomous self-healing
- Performs semantic AI correction
- Creates clean Silver layer datasets
- Generates Gold layer KPIs & analytics
- Produces dynamic visualizations

The architecture follows the traditional:

```text
Bronze → Silver → Gold
```
````

data lakehouse architecture used in modern data engineering systems.

---

# Features

## Autonomous AI Agents

### Profiler Agent

- Understands dataset schema
- Detects rows, columns, datatypes
- Profiles raw datasets

### Rule Generator Agent

- Creates validation rules dynamically
- Identifies required quality checks

### Validator Agent

Detects:

- Null values
- Duplicate rows
- Invalid state codes
- Schema inconsistencies

### Self-Healing Agent

Automatically:

- Removes duplicates
- Repairs invalid values
- Fixes missing values
- Standardizes inconsistent data

### Semantic AI Agent

Uses AI inference to:

- Predict semantic categories
- Improve data consistency
- Infer missing meanings

### Analytics Agent

Generates:

- KPIs
- Revenue analytics
- Customer insights
- Automatic visualizations

---

# Architecture

```text
                Upload CSV Files
                        ↓
              Bronze Layer (Raw)
                        ↓
                Profiler Agent
                        ↓
             Rule Generator Agent
                        ↓
                Validator Agent
                        ↓
               Self-Healing Agent
                        ↓
               Semantic AI Agent
                        ↓
             Silver Layer (Cleaned)
                        ↓
               Analytics Agent
                        ↓
            Gold Layer Dashboards
```

---

# Bronze → Silver → Gold Layers

## Bronze Layer

Stores:

- Raw uploaded datasets
- Original schema
- Unmodified source data

### Purpose

- Preserve original data
- Enable auditability
- Support lineage tracking

---

## Silver Layer

Stores:

- Cleaned datasets
- Validated records
- Repaired values
- Standardized schema

### Processing Includes

- Null handling
- Duplicate removal
- Invalid value correction
- Semantic repair
- Standardization

---

## Gold Layer

Generates:

- Business KPIs
- Revenue analytics
- Customer analytics
- Payment insights
- Dynamic visualizations

### Business Intelligence Includes

- Top customer states
- Top customer cities
- Revenue by payment type
- Average order value
- Payment type distribution
- Dataset quality metrics

---

# Tech Stack

| Technology                | Usage                     |
| ------------------------- | ------------------------- |
| Python                    | Core programming          |
| Streamlit                 | Frontend dashboard        |
| Pandas                    | Data processing           |
| LangGraph                 | Multi-agent orchestration |
| LangChain                 | AI workflow support       |
| OpenAI                    | Semantic inference        |
| Plotly / Streamlit Charts | Visualizations            |

---

# Project Structure

```text
ingestion_quality_agent/
│
├── agents/
│   ├── profiler.py
│   ├── rule_generator.py
│   ├── validator.py
│   ├── healer.py
│   ├── semantic_healer.py
│   └── insights_generator.py
│
├── outputs/
│   ├── bronze/
│   └── silver/
│
├── utils/
│
├── workflow.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

# Multi-Agent Workflow

The system uses LangGraph to orchestrate autonomous AI agents.

## Workflow Execution

```text
Dataset Upload
      ↓
Profiler Agent
      ↓
Rule Generator Agent
      ↓
Validator Agent
      ↓
Self-Healing Agent
      ↓
Semantic AI Agent
      ↓
Analytics Agent
      ↓
Dashboard Generation
```

---

# Automatic Data Quality Checks

The system validates:

- Missing values
- Duplicate records
- Invalid categorical values
- State code consistency
- Schema mismatches
- Datatype inconsistencies

---

# Autonomous Self-Healing

The pipeline automatically performs:

- Duplicate removal
- Invalid state correction
- Missing value handling
- Semantic category inference
- Data standardization

---

# Dynamic Visualizations

The system automatically generates:

- Bar charts
- Line charts
- KPI metrics
- Revenue analytics
- Customer analytics
- Dataset distributions

Even for newly uploaded unknown datasets.

---

# KPIs Generated

The Gold layer automatically creates:

- Top Customer States
- Top Customer Cities
- Revenue by Payment Type
- Payment Type Distribution
- Total Revenue
- Average Order Value
- Total Orders
- Dataset Processing Metrics
- Validation Issue Statistics

---

# Example Datasets Used

- Olist Customers Dataset
- Olist Orders Dataset
- Olist Payments Dataset
- Olist Products Dataset

---

# Installation

## Clone Repository

```bash
git clone <your-github-repo-link>
cd ingestion_quality_agent
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Virtual Environment

### Mac/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Project

```bash
streamlit run streamlit_app.py
```

---

# How to Use

## Step 1

Upload one or more CSV datasets.

---

## Step 2

Click:

```text
Run Autonomous Pipeline
```

---

## Step 3

The AI agents automatically:

- Profile data
- Validate quality
- Detect issues
- Heal corrupted records
- Generate Silver datasets
- Create Gold analytics

---

## Step 4

Explore:

- Bronze Layer
- Silver Layer
- Gold Layer dashboards

---

# Example Business Insights

The platform can automatically identify:

- Highest revenue payment types
- Most active customer regions
- Revenue distributions
- Customer geographic concentration
- Average order spending
- Dataset quality improvements

---

# AI + Data Engineering Concepts Used

This project demonstrates:

## Data Engineering

- Bronze/Silver/Gold architecture
- Data validation pipelines
- Data cleaning
- ETL concepts
- Data quality engineering

## AI Engineering

- Semantic inference
- Autonomous workflows
- Multi-agent systems
- AI-assisted analytics

## Agentic AI

- Decision-based execution
- Self-healing behavior
- Workflow orchestration
- Dynamic processing

---

# Why This Project Matters

Traditional data pipelines require:

- manual validation
- manual cleaning
- manual monitoring

This project introduces:

- autonomous decision-making
- self-healing pipelines
- AI-assisted data quality
- intelligent analytics generation

This simulates modern AI-driven Data Engineering systems used in enterprise platforms.

---

# Future Enhancements

Planned enterprise upgrades:

- Snowflake integration
- MCP integration
- Real-time streaming ingestion
- AI-generated validation rules
- Data lineage tracking
- Pipeline monitoring
- Cloud deployment
- Interactive Plotly dashboards
- Data catalog integration

```

```
