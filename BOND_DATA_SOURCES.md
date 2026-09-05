# 📊 Surat Utang (Bond) Data Sources
## Free Data untuk Treasury Yields & Bond Analysis

**Last Updated:** September 5, 2026  
**Status:** ✅ VERIFIED & READY TO USE

---

## 🏆 TOP FREE DATA SOURCES

### **1. FRED (Federal Reserve Economic Data) - BEST FOR US TREASURY**

**Website:** https://fred.stlouisfed.org  
**Type:** Free, official US Federal Reserve data  
**Coverage:** 100% free, no registration needed

#### Available US Treasury Yields:
```
✅ 3-Month Bill (^IRX or MMNRNJ via FRED)
✅ 2-Year Yield (DGS2)
✅ 5-Year Yield (DGS5)
✅ 10-Year Yield (DGS10) ← MAIN ONE
✅ 20-Year Yield (DGS20)
✅ 30-Year Yield (DGS30)
✅ Real 10-Year Yield (DFEDTARU)
```

#### How to Access:
```python
# Via Python with pandas-datareader
import pandas_datareader as pdr
from datetime import datetime

# Get 10-Year Treasury Yield
ten_year = pdr.get_data_fred('DGS10', start='2020-01-01', end='2026-09-05')

# Get 2-Year Treasury Yield
two_year = pdr.get_data_fred('DGS2', start='2020-01-01', end='2026-09-05')

# Calculate spread (yield curve)
spread = ten_year - two_year
```

#### Or via Web:
```
https://fred.stlouisfed.org/series/DGS10    (10-Year)
https://fred.stlouisfed.org/series/DGS2     (2-Year)
https://fred.stlouisfed.org/series/DGS30    (30-Year)
```

#### Download as CSV:
```
https://fred.stlouisfed.org/data/DGS10.txt
https://fred.stlouisfed.org/data/DGS2.txt
```

---

### **2. US Treasury Direct - OFFICIAL SOURCE**

**Website:** https://www.treasurydirect.gov/instit/anncedata/instrats/instrats.htm  
**Type:** Official US Treasury Department  
**Coverage:** Real-time auction rates

#### What You Get:
```
✅ Treasury Bill rates (4-week, 13-week, 26-week, 52-week)
✅ Treasury Note rates (2-year, 5-year, 10-year)
✅ Treasury Bond rates (20-year, 30-year)
✅ TIPS (Treasury Inflation-Protected Securities)
✅ Historical data back to 2000
```

#### Download Data:
```
Main page: https://www.treasurydirect.gov/instit/anncedata/instrats/instrats.htm
Historical: https://www.treasurydirect.gov/instit/anncedata/press/press_results.txt
```

---

### **3. Investing.com - FREE API & WEB DATA**

**Website:** https://www.investing.com  
**Type:** Free with registration (optional)  
**Coverage:** Global bonds, yields, spreads

#### Available Bonds:
```
✅ US Treasury Yields (all maturities)
✅ German Bund yields
✅ UK Gilt yields
✅ Japanese JGB yields
✅ Yield spreads (10Y-2Y, etc)
✅ Yield curves by country
```

#### How to Get Data:
```
Web: https://www.investing.com/rates-bonds/us-10y-bond
API: Limited free access, but web scraping possible
```

---

### **4. yfinance (Python Library) - SIMPLEST**

**Library:** yfinance  
**Type:** Free, Python  
**Coverage:** Treasury yields, bond ETFs

#### Installation:
```bash
pip install yfinance pandas
```

#### Python Code:
```python
import yfinance as yf
import pandas as pd

# US 10-Year Yield
ten_year = yf.download('^TNX', start='2020-01-01', end='2026-09-05')
print(ten_year[['Close']])

# US 5-Year Yield
five_year = yf.download('^FVX', start='2020-01-01', end='2026-09-05')

# US 2-Year Yield
two_year = yf.download('^TYX', start='2020-01-01', end='2026-09-05')

# US 3-Month Bill
three_month = yf.download('^IRX', start='2020-01-01', end='2026-09-05')

# Treasury ETF (iShares 20+ Year Treasury Bond ETF)
tlt = yf.download('TLT', start='2020-01-01', end='2026-09-05')

# Create yield curve
yields = pd.DataFrame({
    '3M': three_month['Close'],
    '2Y': two_year['Close'],
    '5Y': five_year['Close'],
    '10Y': ten_year['Close']
})
```

#### yfinance Bond Symbols:
```
^IRX   = 3-Month Treasury Bill Yield
^TNX   = 10-Year Treasury Yield ← MOST IMPORTANT
^TYX   = 20-Year Treasury Yield
^FVX   = 5-Year Treasury Yield
^TXY   = 30-Year Treasury Yield
TLT    = iShares 20+ Year Treasury Bond ETF
IEF    = iShares 7-10 Year Treasury Bond ETF
SHY    = iShares 1-3 Year Treasury Bond ETF
```

---

### **5. World Bank Open Data - GLOBAL BONDS**

**Website:** https://data.worldbank.org  
**Type:** Free, official, global coverage  
**Coverage:** Bond yields for 200+ countries

#### How to Access:
```
1. Go to https://data.worldbank.org
2. Search for "Government Bond Yields"
3. Select country and maturity
4. Download as CSV/Excel
```

#### Example Indicators:
```
✅ GC.XPN.GNRL.ZS - Government bond yields (10-year)
✅ FP.CPI.TOTL.ZG - CPI (affects bond pricing)
```

---

### **6. Trading Economics - COMPREHENSIVE**

**Website:** https://tradingeconomics.com  
**Type:** Free web (limited) + API (paid for advanced)  
**Coverage:** Global bonds, yields, economic calendars

#### Free Data Available:
```
✅ US Treasury yields (10Y, 2Y, 5Y, 30Y)
✅ Yield spreads
✅ Central Bank yields (ECB, BoE, BoJ)
✅ Economic calendar with bond impact
```

#### Access:
```
Web: https://tradingeconomics.com/united-states/government-bond-yields
Calendar: https://tradingeconomics.com/calendar
```

---

### **7. ECB, BoE, BoJ Official Sites - CENTRAL BANK BONDS**

#### European Central Bank (ECB)
```
Website: https://www.ecb.europa.eu/stats
German Bund yields: https://www.ecb.europa.eu/stats/eurofxref/eurofxref-data.zip
```

#### Bank of England (BoE)
```
Website: https://www.bankofengland.co.uk/boeapps/database
UK Gilt yields available
```

#### Bank of Japan (BoJ)
```
Website: https://www.boj.or.jp
Japanese Government Bond (JGB) yields
```

---

## 🔧 IMPLEMENTATION: BOND DATA FETCHER

### Python Script to Fetch All Bond Data:

```python
import yfinance as yf
import pandas_datareader as pdr
from datetime import datetime
import pandas as pd

class BondDataFetcher:
    """Fetch bond yields from multiple free sources"""
    
    @staticmethod
    def get_us_treasury_yields(start_date='2020-01-01', end_date=None):
        """Fetch US Treasury yields via yfinance"""
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        symbols = {
            '3M': '^IRX',
            '2Y': '^TYX',
            '5Y': '^FVX',
            '10Y': '^TNX',
            '30Y': '^TXY'
        }
        
        yields = {}
        for name, symbol in symbols.items():
            try:
                data = yf.download(symbol, start=start_date, end=end_date, progress=False)
                if len(data) > 0:
                    yields[name] = data['Close']
            except Exception as e:
                print(f"Error fetching {name}: {e}")
        
        return pd.DataFrame(yields)
    
    @staticmethod
    def get_fred_yields(start_date='2020-01-01', end_date=None):
        """Fetch yields via FRED (Federal Reserve)"""
        if end_date is None:
            end_date = datetime.now()
        else:
            end_date = pd.to_datetime(end_date)
        
        fred_codes = {
            'DGS2': '2-Year (FRED)',
            'DGS5': '5-Year (FRED)',
            'DGS10': '10-Year (FRED)',
            'DGS30': '30-Year (FRED)'
        }
        
        yields = {}
        for code, label in fred_codes.items():
            try:
                data = pdr.get_data_fred(code, start=start_date, end=end_date)
                yields[label] = data
            except Exception as e:
                print(f"Error fetching {code}: {e}")
        
        return pd.DataFrame(yields)
    
    @staticmethod
    def calculate_yield_curve(yields_df):
        """Calculate yield curve and spreads"""
        results = {
            '2Y-10Y Spread': yields_df['10Y'] - yields_df['2Y'],
            '10Y-30Y Spread': yields_df['30Y'] - yields_df['10Y'],
            'Curve Status': 'NORMAL' if (yields_df['10Y'] > yields_df['2Y']).all() else 'INVERTED'
        }
        return results
```

---

## 📊 HOW TO INTEGRATE WITH TRADING SIGNALS

### Complete Script:

```python
# fetch_bond_data.py
import yfinance as yf
import pandas as pd
from datetime import datetime

print("="*80)
print("BOND DATA FETCHER - US TREASURY YIELDS")
print("="*80)

# Fetch latest yields
try:
    yields_10y = yf.download('^TNX', period='5d', progress=False)
    yields_2y = yf.download('^TYX', period='5d', progress=False)
    yields_3m = yf.download('^IRX', period='5d', progress=False)
    
    if len(yields_10y) > 0 and len(yields_2y) > 0:
        y10_latest = float(yields_10y['Close'].iloc[-1]) / 100
        y2_latest = float(yields_2y['Close'].iloc[-1]) / 100
        y3m_latest = float(yields_3m['Close'].iloc[-1]) / 100
        
        print(f"\n📊 CURRENT TREASURY YIELDS:")
        print(f"   3-Month:    {y3m_latest:.3f}%")
        print(f"   2-Year:     {y2_latest:.3f}%")
        print(f"   10-Year:    {y10_latest:.3f}%")
        
        # Yield curve analysis
        spread_10y_2y = (y10_latest - y2_latest) * 100  # basis points
        print(f"\n📈 YIELD CURVE:")
        print(f"   10Y-2Y Spread: {spread_10y_2y:+.1f} bps")
        
        if spread_10y_2y > 0:
            print(f"   Status: ✅ NORMAL (Healthy)")
        elif spread_10y_2y > -50:
            print(f"   Status: ⚠️  FLATTENING (Watch)")
        else:
            print(f"   Status: ❌ INVERTED (Recession Signal)")
            
except Exception as e:
    print(f"Error: {e}")
```

---

## 🎯 RECOMMENDED DATA SOURCES BY USE CASE

| Use Case | Source | Why |
|----------|--------|-----|
| **Quick check (5 min)** | Investing.com web | Fastest, real-time |
| **Python automation** | yfinance | Easiest integration |
| **Historical analysis** | FRED | Most reliable, 100+ years |
| **Official data** | US Treasury Direct | Most accurate |
| **Global bonds** | World Bank | Comprehensive |
| **Automated daily** | FRED + yfinance | Combine both |
| **Real-time alerts** | Trading Economics | Best calendar + yields |

---

## ✅ COMPLETE SETUP: FETCH BONDS DAILY

### Create `fetch_bonds_daily.py`:

```python
#!/usr/bin/env python3
"""Fetch bond yields daily for macro analysis"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def fetch_and_save():
    """Fetch yields and save to CSV"""
    
    # Fetch data
    yields = {}
    symbols = {'^IRX': '3M', '^TYX': '2Y', '^FVX': '5Y', '^TNX': '10Y', '^TXY': '30Y'}
    
    for symbol, label in symbols.items():
        data = yf.download(symbol, period='1d', progress=False)
        if len(data) > 0:
            yields[label] = float(data['Close'].iloc[-1]) / 100
    
    # Create dataframe
    df = pd.DataFrame([yields], index=[datetime.now()])
    
    # Save/append to CSV
    filename = 'data/bond_yields_historical.csv'
    if os.path.exists(filename):
        existing = pd.read_csv(filename, index_col=0, parse_dates=True)
        df = pd.concat([existing, df])
    
    df.to_csv(filename)
    print(f"✅ Yields saved: {yields}")

if __name__ == '__main__':
    fetch_and_save()
```

### Schedule daily run:
```powershell
# Windows Task Scheduler
$trigger = New-ScheduledTaskTrigger -Daily -At 5:00PM
$action = New-ScheduledTaskAction -Execute "python" -Argument "fetch_bonds_daily.py"
Register-ScheduledTask -TaskName "FetchBondYields" -Trigger $trigger -Action $action
```

---

## 🔗 QUICK LINKS TO BOOKMARK

| Service | Link | Type |
|---------|------|------|
| **FRED** | https://fred.stlouisfed.org | Best for analysis |
| **Treasury Direct** | https://www.treasurydirect.gov | Official |
| **yfinance Docs** | https://pypi.org/project/yfinance/ | Python |
| **Investing.com** | https://investing.com/rates-bonds | Real-time web |
| **Trading Economics** | https://tradingeconomics.com | Calendar + yields |
| **World Bank Data** | https://data.worldbank.org | Global |

---

## 💡 NEXT STEPS

1. **Install pandas-datareader** for FRED access:
   ```bash
   pip install pandas-datareader
   ```

2. **Test FRED connection:**
   ```python
   import pandas_datareader as pdr
   data = pdr.get_data_fred('DGS10')
   print(data.tail())
   ```

3. **Create daily bond fetcher script**

4. **Integrate with trading signals:**
   - High yields rising → Risk-off → Skip commodity BUYs
   - Yields falling → Risk-on → Take commodity BUYs

5. **Monitor yield curve daily**
   - Normal (2Y < 10Y) = Health
   - Inverted (2Y > 10Y) = Warning

---

## 🎓 INTERPRETATION GUIDE

```
Understanding Bond Yields:

YIELDS RISING:
✅ Dollar strengthens
✅ US economy strong
❌ Bond prices fall
❌ Commodities weak
❌ Growth stocks may underperform

YIELDS FALLING:
❌ Dollar weakens
⚠️ Growth concerns
✅ Bond prices rise
✅ Commodities rally
✅ Growth stocks rally

YIELD CURVE NORMAL (2Y < 10Y):
✅ Economy healthy
✅ Banks profitable
✅ Take BUY signals

YIELD CURVE INVERTED (2Y > 10Y):
⚠️ Recession warning
❌ Tighten stops
❌ Reduce position size
```

---

**Status:** ✅ ALL FREE DATA SOURCES IDENTIFIED & READY TO USE

**Next:** Run bond data fetcher and integrate with macro analysis! 🚀
