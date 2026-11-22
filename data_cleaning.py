from pathlib import Path

import pandas as pd

RAW = Path("data/raw")
PROCESSED = Path("data/processed")


def clean_nav_history():
    # 1. read from raw
    nh = pd.read_csv(RAW / "02_nav_history.csv")

    print(nh.shape)
    print(nh.dtypes)

    nh["date"] = pd.to_datetime(nh["date"])
    print(nh.dtypes)

    checkDuplicate = nh.duplicated().sum()
    print("Duplicate Count: ", checkDuplicate)
    if checkDuplicate > 0:
        # duplicate present
        nh = nh.drop_duplicates()

    print(nh.shape)

    # sorting by amfi_code and date
    nh = nh.sort_values(["amfi_code", "date"])
    print(nh.head())

    checkPrice = len(nh[nh["nav"] <= 0])
    if checkPrice > 0:
        nh = nh[nh["nav"] > 0]
        print("NAV validation:", checkPrice, "rows with nav <= 0 removed")

    print(nh.shape)

    # forward fill
    CODES = nh["amfi_code"].unique()
    parts = []
    for code in CODES:
        # got only rows with code value as amfi_code
        getData = nh[nh["amfi_code"] == code]
        # set date as row label
        getData = getData.set_index("date")
        # adds every missing calendar day
        getData = getData.asfreq("D")

        # fills with previous value
        getData["nav"] = getData["nav"].ffill()
        getData["amfi_code"] = code
        getData = getData.reset_index()
        parts.append(getData)

    # join all 40 funds into one table
    nh = pd.concat(parts)
    # date goes back to being a column
    nh = nh.reset_index()
    # put the columns in the usual order
    nh = nh[["amfi_code", "date", "nav"]]

    print(nh.shape)  # more than 46000 rows, 3 columns
    print(nh["nav"].isna().sum())  # should be 0
    print(nh.dtypes)  # date should be datetime64

    sizes = nh.groupby("amfi_code").size()
    print(sizes.min(), sizes.max())  # should be the same number

    nh.to_csv(PROCESSED / "02_nav_history.csv", index=False)
    return nh


def clean_investor_transactions():
    it = pd.read_csv(RAW / "08_investor_transactions.csv")
    print(it.shape)
    print(it.dtypes)
    print(it["transaction_type"].unique())
    print(it["kyc_status"].unique())
    print(it["amount_inr"].describe())

    # counts rows where amount <= 0
    checkAmount = len(it[it["amount_inr"] <= 0])
    if checkAmount > 0:
        print(it[it["amount_inr"] <= 0]["transaction_type"].value_counts())

    # transaction_type already consistent
    # kyc_status has 2 valid values (Verified, Pending)
    # 0 rows with amount <= 0
    it["transaction_date"] = pd.to_datetime(it["transaction_date"])
    print(it.dtypes)

    # checking duplicates
    print(it.duplicated().sum())
    it = it.drop_duplicates()  # removed duplicate if any

    it.to_csv(PROCESSED / "08_investor_transactions.csv", index=False)
    return it


def scheme_performance():
    sp = pd.read_csv(RAW / "07_scheme_performance.csv")
    print(sp.shape)
    print(sp.dtypes)

    described = sp.describe()
    for x in described:
        print(f"MAX of {x}", sp[x].max())
        print(f"MIN of {x}", sp[x].min())

    # expense ratio check
    bad = sp[(sp["expense_ratio_pct"] < 0.1) | (sp["expense_ratio_pct"] > 2.5)]
    print("Expense ratio outside 0.1 - 2.5:", len(bad))
    if len(bad) > 0:
        print(bad[["scheme_name", "expense_ratio_pct"]])

    # checking nulls and duplicates
    print(sp.duplicated().sum())
    sp = sp.drop_duplicates()

    print(sp.isna().sum())
    sp = sp.dropna()

    sp.to_csv(PROCESSED / "07_scheme_performance.csv", index=False)
    return sp


# cleaning remaining 7 files
files = [
    "01_fund_master",
    "03_aum_by_fund_house",
    "04_monthly_sip_inflows",
    "05_category_inflows",
    "06_industry_folio_count",
    "09_portfolio_holdings",
    "10_benchmark_indices",
]
dateColms = [
    "date",
    "launch_date",
    "month",
    "portfolio_date",
]

def cleanRemainingFile():
    for file in files:
        df = pd.read_csv(RAW / f"{file}.csv")

        for colms in df:
            if colms in dateColms:
                df[colms] = pd.to_datetime(df[colms])

        print(df.duplicated().sum())
        df = df.drop_duplicates()

        df.to_csv(PROCESSED / f"{file}.csv", index=False)




clean_nav_history()
clean_investor_transactions()
scheme_performance()
cleanRemainingFile()
