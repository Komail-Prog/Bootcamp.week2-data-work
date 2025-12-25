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

Setup & Installation
Prerequisites

Python 3.10+

uv installed
(If not installed:)

pip install uv

Installation Steps

Clone the repository and enter the project folder:

cd week2-data-work


Create and sync the virtual environment:

uv venv
uv sync


Activate the environment:

Windows

.venv\Scripts\activate


macOS / Linux

source .venv/bin/activate

How to Run
Run the ETL Pipeline (Master Switch)

This is the single command to process all data.
It reads from data/raw/, cleans and validates the data, and writes outputs to data/processed/.

python scripts/run_etl.py

Run the EDA Notebook

Open notebooks/eda.ipynb in VS Code

Set the kernel to the .venv created by uv

Run all cells

Visualizations will be exported to:

reports/figures/

Expected Outputs

After running run_etl.py, the data/processed/ folder will contain:

Path	Description
analytics_table.parquet	Primary output: joined, cleaned, and engineered dataset
users_clean.parquet	Standardized and de-duplicated user records
_run_meta.json	Audit receipt: row counts, match rates, and run timestamps
reports/summary.md	Business summary of analytical findings and caveats
FAQ
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