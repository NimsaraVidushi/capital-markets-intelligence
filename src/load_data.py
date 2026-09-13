import pandas as pd
import pyodbc
from pathlib import Path
import os
import sys

# Configuration
# ==========================================
SERVER = os.environ.get('SQL_SERVER', 'LAPTOP-7L2U5JD1')
DATABASE = 'CapitalMarketsDB'

# Connection string using Windows Authentication
CONN_STR = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / 'data' / 'processed' / 'market_data_features.csv'

# Functions


def get_connection():
    try:
        return pyodbc.connect(CONN_STR)
    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {e}")
        print("Please ensure your SQL Server is running and the SERVER variable is correct.")
        sys.exit(1)

def load_dim_security(cursor, df):
    print("Loading DimSecurity...")
    tickers = df['Ticker'].unique()
    
    for ticker in tickers:
        # Check if exists
        cursor.execute("SELECT 1 FROM DimSecurity WHERE Ticker = ?", ticker)
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO DimSecurity (Ticker, CompanyName, AssetType) VALUES (?, ?, ?)",
                ticker, f"{ticker} Corp", "Stock"
            )
    cursor.commit()

def load_fact_market_data(cursor, df):
    print("Loading FactMarketData...")
    
    # Get SecurityKey mapping
    cursor.execute("SELECT SecurityKey, Ticker FROM DimSecurity")
    security_map = {row.Ticker: row.SecurityKey for row in cursor.fetchall()}
    
    # Prepare data for bulk insert
    insert_query = """
    INSERT INTO FactMarketData (
        SecurityKey, TradeDate, OpenPrice, HighPrice, LowPrice, ClosePrice, 
        AdjustedClose, Volume, DailyReturn, Return30D, Volatility30D, 
        AnnualizedVolatility, MA20, MA50, AvgVolume20D, VolumeChange
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    # Convert dataframe to records
    records = []
    for _, row in df.iterrows():
        records.append((
            security_map[row['Ticker']],
            row['Date'],
            row['Open'],
            row['High'],
            row['Low'],
            row['Close'],
            row.get('Adj Close', row['Close']), # Fallback if Adj Close is missing
            row['Volume'],
            row.get('Daily_Return', None),
            row.get('Return_30D', None),
            row.get('Volatility_30D', None),
            row.get('Annualized_Volatility', None),
            row.get('MA20', None),
            row.get('MA50', None),
            row.get('Avg_Volume_20D', None),
            row.get('Volume_Change', None)
        ))
        
    # Replace nan with None for SQL NULL
    records = [[None if pd.isna(x) else x for x in record] for record in records]
    
    # Batch execute
    cursor.executemany(insert_query, records)
    cursor.commit()
    print(f"Inserted {len(records)} rows into FactMarketData.")

def main():
    print(f"Connecting to {SERVER}...")
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Loading dataset...")
    df = pd.read_csv(INPUT_FILE)
    
    load_dim_security(cursor, df)
    
    # Clear existing fact data to avoid duplicates on re-run
    print("Clearing existing FactMarketData...")
    cursor.execute("TRUNCATE TABLE FactMarketData")
    cursor.commit()
    
    load_fact_market_data(cursor, df)
    
    conn.close()
    print("Data loading completed successfully!")

if __name__ == "__main__":
    main()
