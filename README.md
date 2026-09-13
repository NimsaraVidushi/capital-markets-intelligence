# Capital Markets Intelligence Pipeline 

This repository contains an end-to-end data engineering and analytics pipeline designed to extract, process, load, and visualize financial market data. 

The project fetches historical stock data using Yahoo Finance, engineers financial features (like moving averages and volatility), stores the data in a structured SQL database, and uses Power BI to create an interactive dashboard for market analysis.

##  Tech Stack

- **Python**: Core scripting language for data extraction and transformation.
- **Libraries**: `pandas`, `yfinance`, `numpy`, `sqlalchemy`, `pyodbc`.
- **Database**: Microsoft SQL Server (Star Schema architecture).
- **Visualization**: Power BI & Jupyter Notebooks.

## Architecture & Pipeline Flow

The pipeline is managed by a centralized script (`src/main.py`) which orchestrates the following workflow:

1. **Extraction (`download_data.py`)**: Connects to the Yahoo Finance API (`yfinance`) to pull historical daily price and volume data for 19 major tech, finance, healthcare, and energy stocks (from Jan 2024 - Sep 2026).
2. **Cleaning (`clean_data.py`)**: Handles missing values, validates data types, and prepares the raw data for feature engineering.
3. **Feature Engineering (`feature_engineering.py`)**: Calculates critical financial metrics using rolling windows:
   - Daily and 30-Day Returns
   - Moving Averages (20-Day, 50-Day)
   - 30-Day & Annualized Volatility
   - Average 20-Day Volume and Volume Change percentage
4. **Data Loading (`load_data.py`)**: Connects to the SQL Server database via `pyodbc` and loads the data into a normalized star schema featuring `DimSecurity` and `FactMarketData` tables.
5. **Visualization (`CapitalMarkets.pbix`)**: A Power BI dashboard connected to the SQL database to visualize market trends, volatility, and volume anomalies.

##  Project Structure

```text
capital-markets-intelligence/
├── data/
│   ├── raw/                  # Raw CSV files downloaded from yfinance
│   └── processed/            # Cleaned and feature-engineered datasets
├── notebooks/                
│   └── 01_market_eda.ipynb   # Jupyter notebook for Exploratory Data Analysis
├── powerbi/
│   └── CapitalMarkets.pbix   # Power BI Dashboard file
├── sql/
│   └── create_tables.sql     # SQL DDL script to create the Star Schema
├── src/                      # Source code for the ETL pipeline
│   ├── main.py               # Orchestration script
│   ├── download_data.py      
│   ├── clean_data.py
│   ├── feature_engineering.py
│   └── load_data.py
├── .gitignore
├── requirements.txt          # Python dependencies
└── README.md
```

## 🚀 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/capital-markets-intelligence.git
   cd capital-markets-intelligence
   ```

2. **Set up a virtual environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the Database:**
   - Ensure Microsoft SQL Server is running locally.
   - Run the script located in `sql/create_tables.sql` in SSMS (SQL Server Management Studio) or Azure Data Studio to create the `CapitalMarketsDB` database and the tables.
   - Update the `SERVER` variable in `src/load_data.py` (or set a `SQL_SERVER` environment variable) to match your local SQL Server instance name.

##  Usage

To run the entire data pipeline from start to finish, simply execute the main script:

```bash
python src/main.py
```

This will automatically download fresh data, transform it, and upload it into your SQL database. Once complete, you can refresh the Power BI dashboard (`powerbi/CapitalMarkets.pbix`) to view the updated visualizations.

