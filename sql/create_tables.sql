-- Create database
CREATE DATABASE CapitalMarketsDB;
GO

USE CapitalMarketsDB;
GO

-- ==========================================
-- Dimension: Security
-- ==========================================

CREATE TABLE DimSecurity (
    SecurityKey INT IDENTITY(1,1) PRIMARY KEY,
    Ticker VARCHAR(10) NOT NULL UNIQUE,
    CompanyName VARCHAR(100) NOT NULL,
    Sector VARCHAR(50),
    Industry VARCHAR(100),
    AssetType VARCHAR(30)
);
GO

-- ==========================================
-- Fact: Market Data
-- ==========================================

CREATE TABLE FactMarketData (
    MarketDataKey INT IDENTITY(1,1) PRIMARY KEY,
    SecurityKey INT NOT NULL,
    TradeDate DATE NOT NULL,
    OpenPrice DECIMAL(18,4),
    HighPrice DECIMAL(18,4),
    LowPrice DECIMAL(18,4),
    ClosePrice DECIMAL(18,4),
    AdjustedClose DECIMAL(18,4),
    Volume BIGINT,

    DailyReturn DECIMAL(18,8),
    Return30D DECIMAL(18,8),
    Volatility30D DECIMAL(18,8),
    AnnualizedVolatility DECIMAL(18,8),
    MA20 DECIMAL(18,4),
    MA50 DECIMAL(18,4),
    AvgVolume20D BIGINT,
    VolumeChange DECIMAL(18,8),

    CONSTRAINT FK_FactMarketData_DimSecurity
        FOREIGN KEY (SecurityKey)
        REFERENCES DimSecurity(SecurityKey)
);
GO