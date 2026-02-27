import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

PROCESSED_FILE = Path(
    "/Users/apple/projects/stock_etl_project/data/processed/weekly_stock_summary.parquet"
)

if not PROCESSED_FILE.exists():
    raise FileNotFoundError(f"{PROCESSED_FILE} not found")

df = pd.read_parquet(PROCESSED_FILE)
print(f"Loaded {len(df)} rows from {PROCESSED_FILE.name}")

df.columns = df.columns.str.lower().str.strip()

required_columns = [
    'symbol',
    'date',
    'open',
    'high',
    'low',
    'close',
    'volume',
    'daily_return'
]

missing_cols = set(required_columns) - set(df.columns)
if missing_cols:
    raise ValueError(f"Missing columns in parquet file: {missing_cols}")

df = df[required_columns]

df['date'] = pd.to_datetime(df['date'], utc=True)

numeric_cols = [
    'open', 'high', 'low', 'close',
    'volume', 'daily_return'
]

df[numeric_cols] = df[numeric_cols].astype(float)

df = df.dropna(subset=['symbol', 'date'])

DB_USER = "***"
DB_PASSWORD = "***"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "***"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

drop_sql = "DROP TABLE IF EXISTS weekly_stock_summary;"

create_sql = """
CREATE TABLE weekly_stock_summary (
    symbol VARCHAR NOT NULL,
    date TIMESTAMPTZ NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    daily_return DOUBLE PRECISION,
    PRIMARY KEY (symbol, date)
);
"""

with engine.connect() as conn:
    conn.execute(text(drop_sql))
    conn.execute(text(create_sql))
    conn.commit()

print("Table 'weekly_stock_summary' created successfully")

df.to_sql(
    name='weekly_stock_summary',
    con=engine,
    if_exists='append',
    index=False,
    method='multi',
    chunksize=500
)

print(f"{len(df)} rows inserted into 'weekly_stock_summary'")
print("ETL Load Completed Successfully 🚀")
