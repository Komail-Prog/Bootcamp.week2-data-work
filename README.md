Data Engineering Bootcamp — Week 2
Order Analytics Pipeline
Overview

This project is a modular ETL (Extract, Transform, Load) pipeline and EDA suite.
It transforms raw CSV data into high-performance Parquet files, ready for analytics and dashboards.

The pipeline enforces schemas, validates keys, detects outliers, and produces a full data quality audit receipt on every run.

What does this project do?

Speed
Uses uv for ultra-fast dependency management and environment setup.

Reliability
Fail-fast validation for required columns and unique keys (order_id, user_id).

Analytics-ready outputs
Produces joined tables with engineered time features and outlier flags.

Auditability
Every run generates a _run_meta.json file with row counts, match rates, and timestamps.

1. Setup & Installation
Prerequisites

Python 3.10+

uv installed

pip install uv

Installation Steps

Clone the repository and enter the project folder:

cd week2-data-work


Create and sync the virtual environment
This creates a virtual environment and installs all dependencies in seconds.

uv venv
uv sync


Activate the environment

Windows

.venv\Scripts\activate


macOS / Linux

source .venv/bin/activate

2. How to Run
Run the ETL Pipeline (Master Switch)

This command extracts raw CSV data, transforms and validates it, and writes all processed datasets and metadata.

Run the command from inside the scripts/ directory:

cd scripts
uv run run_etl.py

Run the EDA Notebook

Open notebooks/eda.ipynb in VS Code

Set the kernel to the .venv created by uv

Run all cells

Generated figures will be saved to:

reports/figures/

Run the Streamlit Dashboard

From the project root:

uv run streamlit run scripts/app.py

3. Expected Outputs

After running run_etl.py, the data/processed/ folder will contain:

Path	Description
analytics_table.parquet	Primary output: joined, cleaned, and engineered dataset
orders_clean.parquet	Cleaned orders with engineered features and outlier flags
users_clean.parquet	Standardized and de-duplicated user records
_run_meta.json	Audit receipt: row counts, match rates, timestamps
reports/summary.md	Business summary of analytical findings
4. FAQ
What if I get a KeyError?

The pipeline validates that order_id and user_id exist.
Check the headers in your data/raw/*.csv files if the script fails early.

How do I update dependencies?

Add a new dependency with:

uv add <library_name>

Where is the final data?

All final outputs are located in:

data/processed/


Parquet is used because it is significantly smaller than CSV and preserves data types such as dates and numeric values.