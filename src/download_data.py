import pandas as pd
import yfinance as yf
from pathlib import Path

# ==============================
# Project paths
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_FILE = RAW_DIR / "market_data_raw.csv"

RAW_DIR.mkdir(parents=True, exist_ok=True)

# ==============================
# Securities
# ==============================

TICKERS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "GOOGL",
    "AMZN",
    "META",
    "JPM",
    "BAC",
    "V",
    "MA",
    "JNJ",
    "UNH",
    "PFE",
    "WMT",
    "KO",
    "PEP",
    "MCD",
    "XOM",
    "CVX"
]

START_DATE = "2024-01-01"
END_DATE = "2026-09-01"

# ==============================
# Download market data
# ==============================

print("Downloading market data...")

data = yf.download(
    TICKERS,
    start=START_DATE,
    end=END_DATE,
    group_by="ticker",
    auto_adjust=False,
    threads=True
)

# ==============================
# Convert to normal table
# ==============================

all_data = []

for ticker in TICKERS:

    if ticker not in data.columns.get_level_values(0):
        print(f"Warning: No data returned for {ticker}")
        continue

    ticker_data = data[ticker].copy()

    ticker_data = ticker_data.reset_index()

    ticker_data["Ticker"] = ticker

    ticker_data = ticker_data[
        [
            "Date",
            "Ticker",
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume"
        ]
    ]

    all_data.append(ticker_data)

# ==============================
# Combine all securities
# ==============================

df = pd.concat(all_data, ignore_index=True)

# Sort
df = df.sort_values(["Ticker", "Date"])

# ==============================
# Save
# ==============================

df.to_csv(OUTPUT_FILE, index=False)

print("\nData saved successfully.")
print(f"File: {OUTPUT_FILE}")
print(f"Shape: {df.shape}")
print(f"Securities: {df['Ticker'].nunique()}")
print("\nFirst 5 rows:")
print(df.head())