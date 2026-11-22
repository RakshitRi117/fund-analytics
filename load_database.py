from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

# Project locations
BASE_DIR = Path(__file__).resolve().parent
PROCESSED = BASE_DIR / "data" / "processed"
DATABASE = BASE_DIR / "bluestock_mf.db"
SCHEMA_FILE = BASE_DIR / "schema.sql"

# Start with a new database each time this script runs
if DATABASE.exists():
    DATABASE.unlink()

# Create the SQLite database through SQLAlchemy
engine = create_engine(f"sqlite:///{DATABASE}")

# Run the SQL table-creation statements from schema.sql
schema_sql = SCHEMA_FILE.read_text()

with engine.begin() as connection:
    for statement in schema_sql.split(";"):
        if statement.strip():
            connection.exec_driver_sql(statement)


def add_date_key(df, date_column):
    """Create YYYYMMDD number used to join to dim_date."""
    df = df.copy()
    dates = pd.to_datetime(df[date_column])
    df["date_key"] = dates.dt.strftime("%Y%m%d").astype(int)
    return df


# -------------------------
# 1. Load dim_fund
# -------------------------
fund = pd.read_csv(PROCESSED / "01_fund_master.csv")

fund_columns = [
    "amfi_code",
    "fund_house",
    "scheme_name",
    "category",
    "sub_category",
    "plan",
    "launch_date",
    "benchmark",
    "expense_ratio_pct",
    "exit_load_pct",
    "min_sip_amount",
    "min_lumpsum_amount",
    "fund_manager",
    "risk_category",
    "sebi_category_code",
]

fund[fund_columns].to_sql(
    "dim_fund",
    engine,
    if_exists="append",
    index=False
)


# -------------------------
# 2. Build and load dim_date
# -------------------------
date_sources = [
    ("02_nav_history.csv", "date"),
    ("03_aum_by_fund_house.csv", "date"),
    ("04_monthly_sip_inflows.csv", "month"),
    ("05_category_inflows.csv", "month"),
    ("06_industry_folio_count.csv", "month"),
    ("08_investor_transactions.csv", "transaction_date"),
    ("09_portfolio_holdings.csv", "portfolio_date"),
    ("10_benchmark_indices.csv", "date"),
]

all_dates = []

for file_name, column_name in date_sources:
    df = pd.read_csv(PROCESSED / file_name)
    all_dates.append(pd.to_datetime(df[column_name]))

unique_dates = (
    pd.concat(all_dates)
    .dropna()
    .drop_duplicates()
    .sort_values()
)

dim_date = pd.DataFrame({
    "full_date": unique_dates.dt.strftime("%Y-%m-%d")
})

dim_date["date_key"] = unique_dates.dt.strftime("%Y%m%d").astype(int)
dim_date["year"] = unique_dates.dt.year
dim_date["month"] = unique_dates.dt.month
dim_date["day"] = unique_dates.dt.day
dim_date["quarter"] = ((unique_dates.dt.month - 1) // 3) + 1

dim_date = dim_date[
    ["date_key", "full_date", "year", "month", "day", "quarter"]
]

dim_date.to_sql(
    "dim_date",
    engine,
    if_exists="append",
    index=False
)


# -------------------------
# 3. Load fact_nav
# -------------------------
nav = pd.read_csv(PROCESSED / "02_nav_history.csv")
nav = add_date_key(nav, "date")

nav[["amfi_code", "date_key", "nav"]].to_sql(
    "fact_nav",
    engine,
    if_exists="append",
    index=False
)


# -------------------------
# 4. Load fact_transactions
# -------------------------
transactions = pd.read_csv(PROCESSED / "08_investor_transactions.csv")
transactions = add_date_key(transactions, "transaction_date")

transaction_columns = [
    "investor_id",
    "date_key",
    "amfi_code",
    "transaction_type",
    "amount_inr",
    "state",
    "city",
    "city_tier",
    "age_group",
    "gender",
    "annual_income_lakh",
    "payment_mode",
    "kyc_status",
]

transactions[transaction_columns].to_sql(
    "fact_transactions",
    engine,
    if_exists="append",
    index=False
)


# -------------------------
# 5. Load fact_performance
# -------------------------
performance = pd.read_csv(PROCESSED / "07_scheme_performance.csv")

performance_columns = [
    "amfi_code",
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct",
    "alpha",
    "beta",
    "sharpe_ratio",
    "sortino_ratio",
    "std_dev_ann_pct",
    "max_drawdown_pct",
    "aum_crore",
    "expense_ratio_pct",
    "morningstar_rating",
    "risk_grade",
]

performance[performance_columns].to_sql(
    "fact_performance",
    engine,
    if_exists="append",
    index=False
)


# -------------------------
# 6. Load fact_aum
# -------------------------
aum = pd.read_csv(PROCESSED / "03_aum_by_fund_house.csv")
aum = add_date_key(aum, "date")

aum[[
    "date_key",
    "fund_house",
    "aum_lakh_crore",
    "aum_crore",
    "num_schemes"
]].to_sql(
    "fact_aum",
    engine,
    if_exists="append",
    index=False
)


# -------------------------
# 7. Load the remaining cleaned datasets
# -------------------------
extra_files = {
    "04_monthly_sip_inflows.csv": "monthly_sip_inflows",
    "05_category_inflows.csv": "category_inflows",
    "06_industry_folio_count.csv": "industry_folio_count",
    "09_portfolio_holdings.csv": "portfolio_holdings",
    "10_benchmark_indices.csv": "benchmark_indices",
}

for file_name, table_name in extra_files.items():
    df = pd.read_csv(PROCESSED / file_name)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )


# -------------------------
# 8. Verify row counts
# -------------------------
tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum",
    "monthly_sip_inflows",
    "category_inflows",
    "industry_folio_count",
    "portfolio_holdings",
    "benchmark_indices",
]

print("\nDatabase row counts:")

with engine.connect() as connection:
    for table_name in tables:
        row_count = connection.exec_driver_sql(
            f"SELECT COUNT(*) FROM {table_name}"
        ).scalar()

        print(f"{table_name}: {row_count}")

print(f"\nDone. Database created: {DATABASE}")