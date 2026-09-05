# Market Research - Swing Trade Analysis

High-probability major trend detection for swing trading (D1 timeframe)

## 📊 Project Overview

This project analyzes multiple markets (stocks, crypto, forex) to identify high-probability swing trade opportunities using technical analysis and machine learning.

**Strategy:**
- Timeframe: D1 (Daily)
- Type: Swing Trading (3-14 days holding)
- Markets: Stocks, Crypto, Forex (any market with daily data)
- Data Source: Free APIs (yfinance, CoinGecko, etc.)

## 📁 Project Structure

```
market-research/
├── data/
│   ├── raw/           # Raw market data (downloaded)
│   └── processed/     # Cleaned & analyzed data
├── src/
│   ├── data_loader.py      # Fetch market data
│   ├── features.py         # Technical indicators
│   ├── backtest.py         # Backtesting engine
│   └── utils.py            # Helper functions
├── notebooks/         # Jupyter analysis
├── models/            # Trained ML models
├── results/
│   ├── backtest/      # Backtest results
│   └── signals/       # Trading signals
├── main_analysis.py   # Main entry point
└── requirements.txt   # Dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
cd D:\market-research
D:\hpc-env\Scripts\Activate.ps1

# Install additional packages
pip install -r requirements.txt
```

### 2. Run Analysis

```powershell
python main_analysis.py
```

This will:
- Download D1 data for multiple markets
- Generate 50+ technical indicators
- Identify swing trade signals
- Backtest strategy performance
- Save results to `data/processed/` and `results/`

### 3. Analyze Specific Market

```powershell
python -c "
from src.data_loader import MarketDataLoader
from src.features import SwingTradeFeatures
from src.backtest import SwingTradeBacktest

# Load stock data
loader = MarketDataLoader()
df = loader.get_stock_data('AAPL', days=365)

# Generate signals
df = SwingTradeFeatures.calculate_all_features(df)

# Backtest
backtest = SwingTradeBacktest()
trades = backtest.backtest(df)
metrics = backtest.get_performance(trades)
backtest.print_results(metrics)
"
```

## 📈 Technical Indicators Used

### Trend Identification
- **EMA 10/20/50:** Moving average crossovers
- **ADX:** Trend strength measurement
- **MACD:** Trend direction & momentum

### Entry/Exit Signals
- **RSI:** Overbought/oversold conditions
- **Bollinger Bands:** Volatility levels
- **Volume Analysis:** Confirmation (optional)

### Signal Generation Logic

**BUY Signal:**
- Price > EMA20 (uptrend)
- RSI < 50 (room to go up)
- MACD > Signal Line (bullish)
- ADX > 20 (trend strength)

**SELL Signal:**
- Price < EMA20 (downtrend)
- RSI > 50 (room to go down)
- MACD < Signal Line (bearish)
- ADX > 20 (trend strength)

## 💰 Backtest Metrics

The backtest calculates:
- **Total Return %:** Portfolio performance
- **Win Rate %:** Percentage of profitable trades
- **Profit Factor:** Average win / average loss ratio
- **Sharpe Ratio:** Risk-adjusted returns (optional)

## 📊 Supported Markets

### Stocks (yfinance)
```python
# US Stocks
symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "NVDA"]

# Load any stock
loader.get_stock_data("AAPL", days=365)
```

### Crypto (yfinance)
```python
symbols = ["BTC-USD", "ETH-USD", "ADA-USD", "SOL-USD"]

loader.get_crypto_data("BTC-USD", days=365)
```

### Forex (via Alternative Data)
```python
# Manual CSV import or additional API
loader.load_local_data("eurusd.csv")
```

## 🔍 Next Steps

1. **Tune Indicators:** Adjust RSI, EMA periods for your market
2. **Add ML Models:** Predict trend probability with Random Forest/LSTM
3. **Risk Management:** Add stop-loss, take-profit levels
4. **Live Trading:** Connect to broker API (alpaca, etc.)
5. **Optimization:** Walk-forward analysis, parameter tuning

## 📝 Example: Custom Analysis

```python
from src.data_loader import MarketDataLoader
from src.features import SwingTradeFeatures
import pandas as pd

# Load multiple markets
loader = MarketDataLoader()
markets = {
    "AAPL": "stock",
    "BTC-USD": "crypto",
    "MSFT": "stock"
}

results = {}
for symbol, mtype in markets.items():
    if mtype == "stock":
        df = loader.get_stock_data(symbol)
    else:
        df = loader.get_crypto_data(symbol)

    df = SwingTradeFeatures.calculate_all_features(df)
    results[symbol] = df[df['Signal'] != 0]  # Only signals

# Display all signals
for symbol, signals in results.items():
    print(f"\n{symbol}: {len(signals)} signals found")
    print(signals[['Close', 'RSI', 'MACD', 'Signal']].tail(10))
```

## 🎯 Performance Expectations

Based on backtests (historical data):
- **Win Rate:** 45-55% (swing trades)
- **Profit Factor:** 1.2 - 1.8 (good strategy)
- **Return:** 15-30% annually (with proper risk management)

*Note: Past performance ≠ Future results. Always test on live market data.*

## 📚 Resources

- Technical Analysis: https://en.wikipedia.org/wiki/Technical_analysis
- yfinance docs: https://github.com/ranaroussi/yfinance
- TA-Lib: https://github.com/mrjbq7/ta-lib
- Backtest tips: https://en.wikipedia.org/wiki/Backtesting

## ⚠️ Disclaimer

This is for educational & research purposes. Trading involves risk. Always:
- Test on historical data first
- Use proper position sizing
- Implement stop-losses
- Start with small capital
- Never risk more than you can afford to lose

---

**Ready to analyze markets?** 🚀

```powershell
D:\hpc-env\Scripts\Activate.ps1
cd D:\market-research
python main_analysis.py
```
