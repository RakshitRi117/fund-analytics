# Fund Analytics

A Python-based analytics project for exploring mutual-fund data, validating AMFI scheme coverage, and retrieving live NAV values from the MFAPI service.

## Overview

This project provides the first stage of a fund-analytics workflow:

- Ingest and inspect supplied mutual-fund CSV datasets
- Review dataset shapes, data types, sample records, and anomalies
- Explore fund masters, including fund houses, categories, sub-categories, and risk grades
- Validate that AMFI scheme codes in the fund master are represented in NAV history
- Fetch and store current NAV data from the MFAPI API

## Project Structure

```text
fund-analytics/
├── data/
│   └── raw/                  # Local input CSVs — intentionally not tracked by Git
├── dashboard/                # Future dashboard work
├── notebooks/                # Exploratory analysis notebooks
├── reports/                  # Data-quality summaries and reports
├── sql/                      # SQL analysis queries
├── data_ingestion.py         # CSV ingestion and data-quality checks
├── live_nav_fetch.py         # Live NAV retrieval from MFAPI
├── requirements.txt          # Python dependencies
└── .gitignore
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/RakshitRi117/fund-analytics.git
cd fund-analytics
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Data Setup

Place the supplied CSV files in:

```text
data/raw/
```

Raw datasets are excluded from version control through `.gitignore`. This keeps the repository lightweight and avoids publishing source data unintentionally.

## Usage

Run all commands from the project root.

### Run data ingestion and validation

```bash
python data_ingestion.py
```

This script loads the available datasets and supports initial data inspection and quality validation.

### Fetch live NAV values

```bash
python live_nav_fetch.py
```

The live NAV workflow uses the [MFAPI](https://www.mfapi.in/) API. It includes the HDFC Top 100 Direct Growth scheme (`125497`) and can be extended to retrieve NAV values for other schemes.

## Data Quality Focus

Initial validation focuses on:

- CSV structure and column data types
- Missing or inconsistent values
- Dataset-level record counts
- AMFI scheme-code coverage between the fund master and NAV history
- Fund classification fields such as category, sub-category, and risk grade

## Technology Stack

- Python
- Pandas and NumPy
- Matplotlib, Seaborn, and Plotly
- SQLAlchemy
- Requests
- SciPy
- Jupyter

## Roadmap

- Add processed-data pipelines
- Build analytical SQL queries
- Create interactive dashboards
- Add automated tests and data-quality checks
- Expand live NAV tracking and historical performance analysis

## Author

Rakshit
