import os
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import time

API_KEY = "fb252b6b76d37ee60b75c28fe1a892d1"  
BASE_URL = "https://api.marketstack.com/v1/eod"
SYMBOLS = ["AAPL", "MSFT", "GOOGL"]
DATE_FROM = "2024-02-01"
DATE_TO = "2026-02-28"
LIMIT = 100 
SAVE_PATH = Path("/Users/apple/projects/stock_etl_project/data/raw")
SAVE_PATH.mkdir(parents=True, exist_ok=True)  
OUTPUT_FILE = SAVE_PATH / f"daily_stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"

all_data = []
offset = 0

print("Starting data extraction...")

while True:
    params = {
        "access_key": API_KEY,
        "symbols": ",".join(SYMBOLS),
        "date_from": DATE_FROM,
        "date_to": DATE_TO,
        "limit": LIMIT,
        "offset": offset
    }

    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        break

    data = response.json()
    batch = data.get("data", [])

    if not batch:
        print("No more data to fetch.")
        break

    all_data.extend(batch)
    print(f"Fetched {len(batch)} records. Total so far: {len(all_data)}")

    offset += LIMIT
    time.sleep(1)  

df = pd.DataFrame(all_data)

df['date'] = pd.to_datetime(df['date'])
numeric_cols = ['open', 'high', 'low', 'close', 'volume']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.to_parquet(OUTPUT_FILE, engine='pyarrow', index=False)
print(f"Extraction complete! Data saved to {OUTPUT_FILE}")
