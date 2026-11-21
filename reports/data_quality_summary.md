# Data Quality Summary — Day 1

## Scope

The ingestion workflow loaded **16 CSV files**:

- 10 supplied analytical datasets
- 6 NAV extracts for selected mutual-fund schemes

The validation reviewed dataset structure, data types, missing values, duplicate rows, AMFI scheme-code coverage, and NAV-history consistency.

## Dataset Overview

| Dataset | Rows | Columns | Missing values | Duplicate rows |
|---|---:|---:|---:|---:|
| Fund master | 40 | 15 | 0 | 0 |
| NAV history | 46,000 | 3 | 0 | 0 |
| AUM by fund house | 90 | 5 | 0 | 0 |
| Monthly SIP inflows | 48 | 6 | 12 | 0 |
| Category inflows | 144 | 3 | 0 | 0 |
| Industry folio count | 21 | 6 | 0 | 0 |
| Scheme performance | 40 | 19 | 0 | 0 |
| Investor transactions | 32,778 | 13 | 0 | 0 |
| Portfolio holdings | 322 | 8 | 0 | 0 |
| Benchmark indices | 8,050 | 3 | 0 | 0 |

The six individual NAV extracts contain between **3,211 and 3,683 records** each. All fields in those extracts are complete and contain no duplicate rows.

## Key Findings

- The fund master contains **40 schemes** across **10 fund houses**.
- Schemes are classified into **2 top-level categories**, **12 sub-categories**, and **5 risk categories**.
- The core datasets have no missing values and no duplicate records, except for `yoy_growth_pct` in the monthly SIP inflows dataset.
- `yoy_growth_pct` has **12 missing values**. This is likely expected for the earliest twelve months because a prior-year comparison is unavailable; it should be confirmed before using the field in analysis.
- AMFI scheme-code coverage is complete:
  - No fund-master codes are missing from NAV history.
  - No NAV-history codes are missing from the fund master.
- Each fund in the consolidated NAV history has exactly **1,150 NAV records**, indicating consistent historical coverage across the included schemes.
- Dates are currently loaded as strings. They should be converted to datetime values before time-series analysis, returns calculations, or trend visualizations.

## Validation Result

The ingestion and linkage checks completed successfully. The data is suitable for the next phase of analysis, subject to treating the 12 missing SIP year-over-year values appropriately and converting date fields to datetime format during processing.
