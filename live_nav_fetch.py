import requests
from pathlib import Path
import pandas as pd

RAW = Path("data/raw")

# The 6 scheme codes we need info on
CODES = [119551, 120503, 118632, 119092, 120841]

def fetch_nav(code):
	# send request
	r = requests.get(f"https://api.mfapi.in/mf/{code}", timeout = 30)
	r.raise_for_status()           # stop with an error i request failed
	js = r.json()

	print("Code -->", f"{code}", js["meta"]["scheme_name"])

	df = pd.DataFrame(js["data"])
	df["date"] = pd.to_datetime(df["date"], dayfirst = True) # writes dayfirst 20-11-2026
	df["nav"] = pd.to_numeric(df["nav"])
	df["amfi_code"] = code
	return df

for code in CODES:
	df = fetch_nav(code)
	df.to_csv(RAW / f"nav{code}.csv", index = False)
	print("     saved", len(df), "rows")
