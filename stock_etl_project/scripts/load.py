import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

PROCESSED_FILE = Path("/Users/apple/projects/stock_etl_project/data/processed/daily_stock_data.parquet")

df = pd.read_parquet(PROCESSED_FILE)
print(f"Loaded {len(df)} rows from {PROCESSED_FILE.name}")

DB_USER = "apple"
DB_PASSWORD = "newStrongPassword123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "kush"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

create_table_sql = """
CREATE TABLE IF NOT EXISTS daily_stock_data (
    symbol VARCHAR NOT NULL,
    exchange VARCHAR,
    date TIMESTAMPTZ NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    adj_open DOUBLE PRECISION,
    adj_high DOUBLE PRECISION,
    adj_low DOUBLE PRECISION,
    adj_close DOUBLE PRECISION,
    adj_volume DOUBLE PRECISION,
    split_factor DOUBLE PRECISION,
    dividend DOUBLE PRECISION,
    daily_return DOUBLE PRECISION,
    ma_7 DOUBLE PRECISION,
    ma_30 DOUBLE PRECISION,
    PRIMARY KEY (symbol, date)
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_sql))
    conn.commit()
print("Table 'daily_stock_data' created successfully (if not exists)")

numeric_cols = [
    'open', 'high', 'low', 'close', 'volume', 
    'adj_open', 'adj_high', 'adj_low', 'adj_close', 'adj_volume',
    'split_factor', 'dividend', 'daily_return', 'ma_7', 'ma_30'
]

df[numeric_cols] = df[numeric_cols].astype(float)

df.to_sql(
    name='daily_stock_data',
    con=engine,
    if_exists='append',
    index=False,
    method='multi',  
    chunksize=500   
)

print(f"{len(df)} rows inserted into 'daily_stock_data'")