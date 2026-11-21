
import pandas as pd
from pathlib import Path

# Loading all CSV files
RAW = Path("data/raw")
dfs = {}

for f in sorted(RAW.glob("*.csv")):
    df = pd.read_csv(f)
    dfs[f.stem] = df

    print(f"\n===== {f.stem} =====")
    print("Shape:", df.shape)
    print(df.dtypes)
    print(df.head())
    print("Nulls:", df.isna().sum(), "| Duplicates:", df.duplicated().sum())

print("\nFiles Loaded:", len(dfs))


# Checking fund codes
codes = [119551, 120503, 118632, 119092, 120841]
fm = dfs["01_fund_master"]

print("\n===== FUND CODE CHECK =====")
print(fm[fm["amfi_code"].isin(codes)][["amfi_code", "scheme_name"]])


# Checking unique values in fund master
print("\n===== UNIQUE VALUES =====")

for column in ["fund_house", "category", "sub_category", "risk_category"]:
    print(f"\nUnique count ({column}):", fm[column].nunique())
    print(f"Unique {column}:", fm[column].unique())


# Checking links between tables
print("\n===== CHECKING TABLE LINKS =====")

print("Fund Master:", len(fm[fm["amfi_code"] == 119551]["fund_house"]))

nh = dfs["02_nav_history"]
print("NAV History:", len(nh[nh["amfi_code"] == 119551]["nav"]))

it = dfs["08_investor_transactions"]
print("Investor Transactions:", len(it[it["amfi_code"] == 119551]["investor_id"]))


# Comparing fund codes in both tables
setcode_fundMaster = set(fm["amfi_code"])
setcode_navHistory = set(nh["amfi_code"])

codesetFM = setcode_fundMaster - setcode_navHistory
codesetNH = setcode_navHistory - setcode_fundMaster

print("\nCodes in Fund Master but not in NAV History:", codesetFM)
print("Codes in NAV History but not in Fund Master:", codesetNH)


# Checking NAV history count for each fund
print("\n===== NAV HISTORY COUNT =====")

counts = nh.groupby("amfi_code").size()
counts = counts.reindex(fm["amfi_code"], fill_value=0)

lowCount = counts.min()
highCount = counts.max()

print("Minimum Count:", lowCount)
print("Maximum Count:", highCount)

if lowCount == highCount:
    print("All funds have the same number of NAV records.")
else:
    print("Some funds have less NAV history.")

    lessHistory = counts[counts < highCount]

    print("\nFunds with less NAV history:")
    print(fm[fm["amfi_code"].isin(lessHistory.index)]
          [["amfi_code", "scheme_name"]])
