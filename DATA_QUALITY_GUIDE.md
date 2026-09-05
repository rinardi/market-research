# Data Quality & Management Guide

**Purpose:** Ensure long-term data reliability and quality for swing trading analysis  
**Updated:** 2026-09-05

---

## 📋 Quick Summary

| Aspect | Status | Details |
|--------|--------|---------|
| **Data Source** | ✅ FREE | yfinance (Yahoo Finance API) |
| **Historical Coverage** | ✅ EXCELLENT | 45+ years available |
| **Current Data** | ✅ 1 YEAR | ~250-365 rows per asset |
| **Recommended** | 🔄 5-10 YEARS | Better backtesting & pattern recognition |
| **Update Frequency** | ✅ DAILY | After market close (5 PM EST) |
| **Reliability** | ✅ 98%+ | Yahoo Finance infrastructure |

---

## 🚀 Quick Start: Fetch Extended Data

### Option 1: Automated Script (Recommended)
```powershell
# Activate environment
D:\hpc-env\Scripts\Activate.ps1
cd D:\market-research

# Run extended data fetcher
python fetch_extended_data.py

# Choose:
# 1 = 2 years
# 2 = 5 years (recommended)
# 3 = 10 years
```

This will:
- Fetch 5-10 years of historical data for all assets
- Validate data integrity
- Save to `data/raw/` 
- Ready for backtesting immediately

### Option 2: Manual with Python
```python
from src.data_loader import MarketDataLoader

loader = MarketDataLoader()

# Get 5 years of NASDAQ data
df = loader.get_index_data(
    '^IXIC',
    start_date='2021-01-01',
    end_date='2026-09-05'
)

# Get 10 years of Bitcoin data
df = loader.get_crypto_data(
    'BTC-USD',
    start_date='2016-01-01',
    end_date='2026-09-05'
)
```

### Option 3: Extend Just the Current Data
```python
# Default is 1 year - extend to 5 years
loader.get_index_data('^IXIC', days=1825)  # 5 years
loader.get_index_data('^IXIC', days=3650)  # 10 years
```

---

## 📊 Data Specifications

### Supported Asset Classes

#### Stock Indices
```
Symbol   Name              Volatility  Years Available
^IXIC    NASDAQ-100        ⭐⭐⭐⭐⭐  45+ years
^GSPC    S&P 500           ⭐⭐⭐⭐   45+ years
^DJI     Dow Jones         ⭐⭐⭐    45+ years
^FTSE    FTSE 100          ⭐⭐⭐⭐   45+ years
^N225    Nikkei 225        ⭐⭐⭐⭐   45+ years
^HSIO    Hang Seng         ⭐⭐⭐    45+ years

Trading Hours: 9:30 AM - 4:00 PM EST (252 trading days/year)
```

#### Commodities
```
Symbol   Name              Volatility  Years Available
GC=F     Gold (Spot)       ⭐⭐⭐⭐⭐  36+ years (~1980s)
CL=F     Oil (WTI)         ⭐⭐⭐⭐⭐  36+ years
NG=F     Natural Gas       ⭐⭐⭐⭐   20+ years
SI=F     Silver            ⭐⭐⭐⭐   36+ years

Trading Hours: 24/5 (Sunday 6 PM - Friday 5 PM EST)
Note: Includes gaps on weekends
```

#### Forex Pairs
```
Symbol     Name        Volatility  Years Available
EURUSD=X   EUR/USD     ⭐⭐⭐⭐   21+ years (~2005)
GBPUSD=X   GBP/USD     ⭐⭐⭐⭐⭐  21+ years
USDJPY=X   USD/JPY     ⭐⭐⭐⭐⭐  21+ years
AUDUSD=X   AUD/USD     ⭐⭐⭐⭐   21+ years
NZDUSD=X   NZD/USD     ⭐⭐⭐    21+ years
USDCAD=X   USD/CAD     ⭐⭐⭐    21+ years
GBPJPY=X   GBP/JPY     ⭐⭐⭐⭐   21+ years
EURJPY=X   EUR/JPY     ⭐⭐⭐⭐   21+ years

Trading Hours: 24/5 (Monday 5 PM - Friday 4 PM EST)
```

#### Cryptocurrency
```
Symbol    Name         Volatility  Years Available
BTC-USD   Bitcoin      ⭐⭐⭐⭐⭐  12+ years (~2014)
ETH-USD   Ethereum     ⭐⭐⭐⭐   7+ years (~2017)

Trading Hours: 24/7 (continuous)
Note: 365 days/year (no weekends/holidays)
```

---

## ✅ Data Validation

### Automatic Validation (Recommended)

```python
from src.data_validator import DataValidator

# Load data
df = pd.read_csv('data/raw/IXIC.csv', index_col=0, parse_dates=True)

# Run full validation
result = DataValidator.full_validation(df, asset_name="NASDAQ-100")

# Result returns:
# {
#   'result': 'PASS' or 'ISSUES',
#   'issues': [list of detected issues],
#   'rows': number of data points,
#   'date_range': (start_date, end_date)
# }
```

### What Gets Validated

✅ **OHLC Relationships** - High ≥ Close ≥ Open ≥ Low  
✅ **Missing Values** - No NaN or null data  
✅ **Volume Data** - No zero/negative volumes  
✅ **Price Range** - Detect unrealistic moves  
✅ **Date Continuity** - No gaps in trading days  
✅ **Data Freshness** - Check if data is current  
✅ **Column Structure** - All required columns present  

### Manual Validation Checklist

```
□ Data rows > 250 (at least 1 year of trading days)
□ Date range is continuous (no gaps > 2 days)
□ No zero or negative volumes
□ High ≥ Low for all rows
□ Close is between High and Low
□ No missing values (NaN)
□ Decimal precision > 2 places
□ Column headers: Open, High, Low, Close, Volume
```

---

## 📈 Recommended Data Configuration

### For Optimal Backtesting
```python
# MINIMUM: 2 years of data
min_years = 2
min_days = min_years * 365

# RECOMMENDED: 5 years of data (multiple cycles)
recommended_years = 5
recommended_days = recommended_years * 365

# MAXIMUM: 10 years of data (complete market cycles)
max_years = 10
max_days = max_years * 365

# Updated main_analysis.py:
days_param = 1825  # 5 years (recommended)
```

### For Different Scenarios
```python
# Scenario 1: Quick testing (minimum)
days = 365  # 1 year

# Scenario 2: Good backtesting (recommended)
days = 1825  # 5 years

# Scenario 3: Deep analysis (comprehensive)
days = 3650  # 10 years

# Scenario 4: Extended research
start_date = '2010-01-01'  # 16+ years
end_date = '2026-09-05'
```

---

## 🔄 Data Update Strategy

### Daily Updates (Recommended for Trading)

**Automation Setup:**
```powershell
# Run automatically every day at 5 PM EST (after market close)
python -c "
from src.data_loader import MarketDataLoader
loader = MarketDataLoader()

# Update each asset with latest day
loader.get_index_data('^IXIC', days=1825)  # 5 years
loader.get_commodity_data('GC=F', days=1825)
loader.get_crypto_data('BTC-USD', days=1825)
"
```

**Using Existing Scheduler:**
```powershell
# Edit scheduler.py to add data refresh
# Update: run_daily_analysis.bat (Windows scheduled task)

# Or use setup_scheduler.ps1 for automated setup
.\setup_scheduler.ps1
```

### Update Frequency Recommendations
```
Stock Indices:    Daily (after 4 PM EST market close)
Commodities:      Daily (24/5 trading)
Forex:           Daily (24/5 trading)
Crypto:          Daily (24/7 trading)

Batch Frequency:  Once per day (combine all updates)
Retention:        Keep full 5-10 years history
```

---

## 🛡️ Data Quality Monitoring

### Automated Health Checks

Add to your automation script:
```python
from src.data_validator import DataValidator
from datetime import datetime

def check_data_health():
    """Daily data health check"""
    
    assets = {
        'NASDAQ': ('data/raw/IXIC.csv', 'NASDAQ-100'),
        'Bitcoin': ('data/raw/BTC_USD.csv', 'Bitcoin'),
        'Gold': ('data/raw/GC.csv', 'Gold'),
    }
    
    issues_found = []
    
    for key, (filepath, name) in assets.items():
        try:
            df = pd.read_csv(filepath, index_col=0, parse_dates=True)
            result = DataValidator.full_validation(df, name, verbose=False)
            
            if result['result'] != 'PASS':
                issues_found.append({
                    'asset': name,
                    'issues': result['issues']
                })
        except Exception as e:
            issues_found.append({
                'asset': name,
                'error': str(e)
            })
    
    # Log or alert on issues
    if issues_found:
        print(f"[ALERT] Data quality issues detected on {datetime.now()}")
        for issue in issues_found:
            print(f"  • {issue}")
    
    return issues_found
```

---

## 🚨 Troubleshooting

### Problem: yfinance API Timeout

**Cause:** Network issue or Yahoo Finance temporary downtime  
**Solution:**
```python
import time
from requests.exceptions import RequestException

def get_data_with_retry(symbol, max_retries=3):
    """Retry logic for flaky connections"""
    for attempt in range(max_retries):
        try:
            df = yf.download(symbol, start=start, end=end)
            return df
        except RequestException:
            if attempt < max_retries - 1:
                wait = (2 ** attempt)  # Exponential backoff
                print(f"Retry {attempt+1}/{max_retries}, waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
```

### Problem: Missing Data Points

**Cause:** Weekends, holidays, or market closures  
**Solution:** Expected behavior (normal). yfinance handles this automatically.

### Problem: Extreme Price Spikes

**Cause:** Stock splits, dividend adjustments, or data errors  
**Solution:**
```python
# Check for known issues
df = df[df['Close'] > 0]  # Remove invalid prices
df = df[(df['High'] >= df['Low'])]  # Verify OHLC
```

### Problem: Data File Too Large

**Cause:** 10+ years × multiple symbols  
**Solution:**
```python
# Compress older data (keep last 5 years active)
# Archive historical data to separate folder

# Or split by year:
def split_data_by_year(df, output_dir='data/archive'):
    for year in df.index.year.unique():
        year_data = df[df.index.year == year]
        year_data.to_csv(f'{output_dir}/{asset}_{year}.csv')
```

---

## 📚 Reference: Data Loading Examples

### Load All Assets with Extended History
```python
from src.data_loader import MarketDataLoader
from datetime import datetime, timedelta

loader = MarketDataLoader()
end_date = datetime.now()
start_date = end_date - timedelta(days=1825)  # 5 years

# Indices
nasdaq = loader.get_index_data('^IXIC', start_date=start_date, end_date=end_date)
sp500 = loader.get_index_data('^GSPC', start_date=start_date, end_date=end_date)

# Commodities
gold = loader.get_commodity_data('GC=F', start_date=start_date, end_date=end_date)
oil = loader.get_commodity_data('CL=F', start_date=start_date, end_date=end_date)

# Forex
eurusd = loader.get_forex_data('EURUSD=X', start_date=start_date, end_date=end_date)

# Crypto
btc = loader.get_crypto_data('BTC-USD', start_date=start_date, end_date=end_date)
```

### Load Specific Date Range
```python
# Last 3 years of Bitcoin
btc = loader.get_crypto_data(
    'BTC-USD',
    start_date='2023-09-05',
    end_date='2026-09-05'
)
```

### Load from Cache (Local File)
```python
df = loader.load_local_data('data/raw/IXIC.csv')
```

---

## 🎯 Summary: Best Practices

✅ **DO:**
- Use yfinance (free, reliable, 45+ years coverage)
- Fetch 5-10 years of historical data for backtesting
- Validate data integrity before analysis
- Update daily after market close
- Keep data locally cached (backup)
- Monitor data freshness regularly

❌ **DON'T:**
- Rely on only 1 year of data (insufficient pattern recognition)
- Use unstable/paid APIs unless absolutely necessary
- Ignore data quality warnings/issues
- Skip validation step before trading
- Update too frequently (once daily is enough)
- Delete raw data files (keep for audit trail)

---

## 📞 Support

**yfinance Documentation:** https://github.com/ranaroussi/yfinance  
**Yahoo Finance:** https://finance.yahoo.com  
**Data Formats:** OHLCV (Open, High, Low, Close, Volume)  

---

**Next Steps:**
1. Run `python fetch_extended_data.py` to get 5-10 years of history
2. Run validation with `python -c "from src.data_validator import DataValidator; ..."`
3. Start backtesting with full historical data
4. Schedule daily updates for live trading

**Status:** ✅ Data sources verified, reliable, and ready for production use.
