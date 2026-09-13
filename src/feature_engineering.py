import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================
# Project paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "market_data_clean.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "market_data_features.csv"

# ==========================================
# Load cleaned data
# ==========================================

print("Loading cleaned market data...")
print(f"Looking for file: {INPUT_FILE}")

df = pd.read_csv(INPUT_FILE)

df["Date"] = pd.to_datetime(df["Date"])

print(f"Input data shape: {df.shape}")

# ==========================================
# Sort data
# ==========================================

df = df.sort_values(["Ticker", "Date"]).reset_index(drop=True)

# ==========================================
# 1. Daily Return
# ==========================================

df["Daily_Return"] = (
    df.groupby("Ticker")["Close"]
    .pct_change()
)

# ==========================================
# 2. 30-Day Return
# ==========================================

df["Return_30D"] = (
    df.groupby("Ticker")["Close"]
    .pct_change(periods=30)
)

# ==========================================
# 3. 20-Day Moving Average
# ==========================================

df["MA20"] = (
    df.groupby("Ticker")["Close"]
    .transform(lambda x: x.rolling(window=20).mean())
)

# ==========================================
# 4. 50-Day Moving Average
# ==========================================

df["MA50"] = (
    df.groupby("Ticker")["Close"]
    .transform(lambda x: x.rolling(window=50).mean())
)

# ==========================================
# 5. 30-Day Volatility
# ==========================================

df["Volatility_30D"] = (
    df.groupby("Ticker")["Daily_Return"]
    .transform(lambda x: x.rolling(window=30).std())
)

# ==========================================
# 6. Annualized Volatility
# ==========================================

df["Annualized_Volatility"] = (
    df["Volatility_30D"] * np.sqrt(252)
)

# ==========================================
# 7. 20-Day Average Trading Volume
# ==========================================

df["Avg_Volume_20D"] = (
    df.groupby("Ticker")["Volume"]
    .transform(lambda x: x.rolling(window=20).mean())
)

# ==========================================
# 8. Volume Change
# ==========================================

df["Volume_Change"] = (
    df["Volume"] / df["Avg_Volume_20D"] - 1
)

# ==========================================
# Save feature-engineered data
# ==========================================

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

# ==========================================
# Display results
# ==========================================

print("\n==========================================")
print("Feature engineering completed successfully!")
print("==========================================")

print(f"Output shape: {df.shape}")

print(f"Number of securities: {df['Ticker'].nunique()}")

print("\nNew features:")
print([
    "Daily_Return",
    "Return_30D",
    "MA20",
    "MA50",
    "Volatility_30D",
    "Annualized_Volatility",
    "Avg_Volume_20D",
    "Volume_Change"
])

print("\nSample results:")
print(
    df[
        [
            "Date",
            "Ticker",
            "Close",
            "Daily_Return",
            "Return_30D",
            "MA20",
            "MA50",
            "Annualized_Volatility",
            "Volume_Change"
        ]
    ].tail(10)
)

print(f"\nSaved to:")
print(OUTPUT_FILE)