import pandas as pd
from pathlib import Path
import numpy as np


RAW_FILE = Path("/Users/apple/projects/stock_etl_project/data/raw")  # Folder with raw Parquet
PROCESSED_FOLDER = Path("/Users/apple/projects/stock_etl_project/data/processed")
PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

raw_files = sorted(RAW_FILE.glob("*.parquet"))
if not raw_files:
    raise FileNotFoundError("No raw Parquet files found in data/raw/")
RAW_FILE_PATH = raw_files[-1]

df = pd.read_parquet(RAW_FILE_PATH)
print(f"Loaded {len(df)} rows from {RAW_FILE_PATH.name}")

df['date'] = pd.to_datetime(df['date'])
numeric_cols = ['open', 'high', 'low', 'close', 'volume']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

df.sort_values(['symbol', 'date'], inplace=True)
df.drop_duplicates(subset=['symbol', 'date'], inplace=True)

for col in numeric_cols:
    def fill_lead_lag(series):
        series = series.copy()
        for i in range(len(series)):
            if pd.isna(series.iloc[i]):
                prev_val = series.iloc[i-1] if i > 0 else np.nan
                next_val = series.iloc[i+1] if i < len(series)-1 else np.nan
                values = [v for v in [prev_val, next_val] if pd.notna(v)]
                series.iloc[i] = np.mean(values) if values else np.nan
        return series

    df[col] = df.groupby('symbol')[col].transform(fill_lead_lag)

df['daily_return'] = (df['close'] - df['open']) / df['open']

df['ma_7'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(7, min_periods=1).mean())
df['ma_30'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(30, min_periods=1).mean())

weekly = df.groupby(['symbol', pd.Grouper(key='date', freq='W')]).agg({
    'open':'mean',
    'high':'max',
    'low':'min',
    'close':'mean',
    'volume':'sum',
    'daily_return':'mean'
}).reset_index()

monthly = df.groupby(['symbol', pd.Grouper(key='date', freq='M')]).agg({
    'open':'mean',
    'high':'max',
    'low':'min',
    'close':'mean',
    'volume':'sum',
    'daily_return':'mean'
}).reset_index()

daily_file = PROCESSED_FOLDER / "daily_stock_data.parquet"
weekly_file = PROCESSED_FOLDER / "weekly_stock_summary.parquet"
monthly_file = PROCESSED_FOLDER / "monthly_stock_summary.parquet"

df.to_parquet(daily_file, engine='pyarrow', index=False)
weekly.to_parquet(weekly_file, engine='pyarrow', index=False)
monthly.to_parquet(monthly_file, engine='pyarrow', index=False)

print(f"Processed daily data saved to {daily_file}")
print(f"Weekly summary saved to {weekly_file}")
print(f"Monthly summary saved to {monthly_file}")
