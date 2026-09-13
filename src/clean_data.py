import pandas as pd
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# File paths
INPUT_FILE = BASE_DIR / "data" / "raw" / "market_data_raw.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "market_data_clean.csv"

print("Loading raw market data...")
print(f"Looking for file: {INPUT_FILE}")

# Load raw data
df = pd.read_csv(INPUT_FILE)

print(f"Raw data shape: {df.shape}")

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Check duplicates
print("\nDuplicate rows:")
print(df.duplicated().sum())

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Remove duplicate rows
df = df.drop_duplicates()

# Required columns
required_columns = [
    "Date",
    "Ticker",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]

# Remove rows missing important values
df = df.dropna(subset=required_columns)

# Sort data
df = df.sort_values(["Ticker", "Date"])

# Reset index
df = df.reset_index(drop=True)

# Create processed folder if it doesn't exist
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Save cleaned data
df.to_csv(OUTPUT_FILE, index=False)

print("\n===================================")
print("Cleaning completed successfully!")
print("===================================")
print(f"Clean data shape: {df.shape}")
print(f"Number of securities: {df['Ticker'].nunique()}")
print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
print(f"Saved to: {OUTPUT_FILE}")