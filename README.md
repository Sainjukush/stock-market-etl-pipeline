# Stock Market ETL Pipeline

## Overview
A comprehensive ETL (Extract, Transform, Load) pipeline for stock market data analysis. This project extracts daily stock data from the Marketstack API for AAPL, MSFT, and GOOGL, transforms it with technical indicators, and loads it into PostgreSQL for analysis.

## Features
- **Data Extraction**: Automated fetching from Marketstack API with pagination
- **Data Transformation**: 
  - Missing value imputation using lead/lag averaging
  - Daily return calculations
  - Moving averages (7-day and 30-day)
  - Weekly and monthly aggregations
- **Data Loading**: PostgreSQL database storage with proper schema
- **Analysis**: Jupyter notebooks for correlation analysis and price trend visualization

## Project Structure
```
stock_etl_project/
├── data/
│   ├── raw/              # Raw data from API (Parquet format)
│   ├── processed/        # Transformed data
│   └── output/           # Analysis outputs (CSV)
├── scripts/
│   ├── extract.py        # API data extraction
│   ├── transform.py      # Data transformation
│   ├── load.py          # Daily data loader
│   ├── load_weeekly.py  # Weekly data loader
│   └── load_monthly.py  # Monthly data loader
├── notebooks/
│   ├── correaltion.ipynb    # Correlation analysis
│   └── Price_trend.ipynb    # Price trend visualization
└── requirements.txt
```

## Prerequisites
- Python 3.8+
- PostgreSQL database
- Marketstack API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Sainjukush/stock-market-etl-pipeline.git
cd stock-market-etl-pipeline
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:
```sql
CREATE DATABASE kush;
CREATE USER apple WITH PASSWORD '********';
GRANT ALL PRIVILEGES ON DATABASE kush TO apple;
```

## Configuration

Update the following variables in the scripts:

**extract.py**:
- `API_KEY`: Your Marketstack API key
- `SYMBOLS`: Stock symbols to track
- `DATE_FROM` / `DATE_TO`: Date range

**Database connection** (in load scripts):
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `DB_HOST`: Database host
- `DB_PORT`: Database port
- `DB_NAME`: Database name

## Usage

### 1. Extract Data
```bash
python stock_etl_project/scripts/extract.py
```
Fetches stock data from Marketstack API and saves to `data/raw/` as Parquet files.

### 2. Transform Data
```bash
python stock_etl_project/scripts/transform.py
```
Processes raw data:
- Handles missing values
- Calculates daily returns
- Computes moving averages
- Creates weekly/monthly summaries
- Saves to `data/processed/`

### 3. Load Data
```bash
# Load daily data
python stock_etl_project/scripts/load.py

# Load weekly data
python stock_etl_project/scripts/load_weeekly.py

# Load monthly data
python stock_etl_project/scripts/load_monthly.py
```

### 4. Run Analysis
Open Jupyter notebooks:
```bash
jupyter notebook stock_etl_project/notebooks/
```

## Database Schema

### daily_stock_data
- `symbol` (VARCHAR): Stock ticker
- `exchange` (VARCHAR): Exchange name
- `date` (TIMESTAMPTZ): Trading date
- `open`, `high`, `low`, `close` (DOUBLE PRECISION): Price data
- `volume` (DOUBLE PRECISION): Trading volume
- `split_factor`, `dividend` (DOUBLE PRECISION): Corporate actions
- `daily_return` (DOUBLE PRECISION): Daily return percentage
- `ma_7`, `ma_30` (DOUBLE PRECISION): Moving averages
- Primary Key: (`symbol`, `date`)

### weekly_stock_summary & monthly_stock_summary
- `symbol` (VARCHAR): Stock ticker
- `date` (TIMESTAMPTZ): Period end date
- `open` (DOUBLE PRECISION): Average opening price
- `high` (DOUBLE PRECISION): Maximum high price
- `low` (DOUBLE PRECISION): Minimum low price
- `close` (DOUBLE PRECISION): Average closing price
- `volume` (DOUBLE PRECISION): Total volume
- `daily_return` (DOUBLE PRECISION): Average daily return
- Primary Key: (`symbol`, `date`)

## Analysis Examples

### Correlation Analysis
The correlation notebook explores relationships between:
- Price metrics (open, high, low, close)
- Volume and daily returns
- 7-day rolling correlations

### Price Trend Analysis
Visualizations include:
- Daily/weekly/monthly close prices
- Trading volume over time
- Daily return distributions
- Cumulative returns

## Data Flow
```
Marketstack API → Extract (Parquet) → Transform → Load → PostgreSQL → Analysis
```

## Output Files
- `data/output/daily_stock_data.csv`
- `data/output/weekly_stock_summary.csv`
- `data/output/monthly_stock_summary.csv`

## Dependencies
- pandas==2.0.3
- numpy==1.24.3
- yfinance==0.2.28
- requests==2.31.0
- sqlalchemy==2.0.19
- psycopg2-binary==2.9.6
- python-dotenv==1.0.0
- pytest==7.4.0

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is open source and available under the MIT License.

## Author
Sainjukush

## Acknowledgments
- Marketstack API for stock data
- PostgreSQL for data storage
- Pandas and NumPy for data processing
