# Dashboard & Notifications - Quick Start

Get real-time market monitoring and Telegram alerts in 5 minutes!

---

## 🚀 QUICK SETUP (5 minutes)

### 1. Get Telegram Credentials (2 min)

**Get Bot Token:**
1. Open Telegram → Find `@BotFather`
2. Send `/newbot`
3. Copy the token (e.g., `123456789:ABC...`)

**Get Chat ID:**
1. Open Telegram → Find `@userinfobot`
2. Send `/start`
3. Copy your User ID (e.g., `987654321`)

### 2. Configure .env (1 min)

1. Rename `.env.example` to `.env`
2. Edit and add your credentials:
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklmnoPQRstuvWXYZ
   TELEGRAM_CHAT_ID=987654321
   ```

### 3. Install & Test (2 min)

```powershell
D:\hpc-env\Scripts\Activate.ps1
pip install -r requirements.txt
python src/notifier.py
```

Check your Telegram for test messages!

---

## 📊 DAILY WORKFLOW

### Option 1: Manual (Best for first time)

```powershell
# Terminal 1: Run analysis
D:\hpc-env\Scripts\Activate.ps1
python main_analysis.py

# Terminal 2: Update dashboard + send Telegram
python update_dashboard.py

# Open dashboard in browser
start dashboard.html
```

**Time:** ~5-10 minutes per day

### Option 2: Automated (Recommended)

```powershell
D:\hpc-env\Scripts\Activate.ps1
python scheduler.py
```

Runs automatically every day at 09:00 AM and 05:00 PM

---

## 📱 WHAT YOU'LL GET

### Telegram Messages:

**Daily Summary (09:00 AM)**
```
SWING TRADING MONITOR
Oil WTI +46.31% [BUY]
Gold -4.57% [SELL]
Bitcoin -12.04% [BUY]
...
```

**Trade Alerts (Real-time)**
```
🟢 BUY SIGNAL: NASDAQ-100
Price: $22,017.85
RSI: 35.5 | MACD: -150.23 | ADX: 28.5
Action: BUY | Risk: 1-2% per trade
```

### Dashboard (HTML)

Open `dashboard.html` to see:
- Live market prices
- Returns % (green = profit, red = loss)
- Win rates and total trades
- Signal status (BUY/SELL/HOLD)
- Portfolio summary

---

## 🎯 TRADING CHECKLIST

Every morning:
- [ ] Check Telegram notification
- [ ] Open dashboard.html to see signals
- [ ] Review indicators (RSI, MACD, ADX)
- [ ] Enter trades per signals
- [ ] Monitor D1 timeframe only
- [ ] Use 1-2% risk per trade
- [ ] Set stop losses

---

## 📈 SIGNAL INTERPRETATION

### BUY Signal (Green)
- Price above EMA20
- RSI < 50 (recovering from oversold)
- MACD above signal line
- ADX > 20 (strong trend)

**Action:** Enter long position ↗️

### SELL Signal (Red)
- Price below EMA20
- RSI > 50 (recovering from overbought)
- MACD below signal line
- ADX > 20 (strong trend)

**Action:** Exit position / Enter short ↘️

### HOLD Signal (Yellow)
- Indicators not aligned
- Waiting for confirmation

**Action:** Stay in cash 🛑

---

## 💡 TIPS

1. **Best Markets for Signals:**
   - Oil WTI (most volatile)
   - Gold (safe haven)
   - NASDAQ (tech stocks)

2. **Trading Hours:**
   - US Market: 9:30 AM - 4:00 PM EST
   - Forex: 24/5 (best Asia/EU overlap)
   - Crypto: 24/7

3. **Position Sizing:**
   - Risk 1-2% per trade
   - If account $10,000 → max risk $100-200
   - Scale size based on ATR (volatility)

4. **Risk Management:**
   - Always use stop loss
   - Never average down losing trades
   - Close at signal reversal

---

## ⚙️ CUSTOMIZATION

### Change Analysis Times

Edit `scheduler.py`:
```python
schedule.every().day.at("09:00").do(daily_job)  # Change time
schedule.every().day.at("17:00").do(daily_job)  # Add more runs
```

### Change Markets Analyzed

Edit `main_analysis.py` - modify indices/commodities/forex lists:
```python
indices = [
    ("^IXIC", "NASDAQ-100"),  # Keep or remove
    ("^GSPC", "S&P 500"),      # Add custom markets
]
```

### Change Trading Strategy

Edit `src/features.py` - modify `generate_swing_signals()`:
- Adjust RSI levels (currently 30/70)
- Adjust ADX threshold (currently 20)
- Add more indicators (Bollinger Bands, Stochastic, etc.)

---

## 🐛 TROUBLESHOOTING

**No Telegram messages?**
```powershell
# Test connection
python src/notifier.py

# Check .env file
cat .env
```

**Dashboard not updating?**
```powershell
# Make sure CSV files exist
ls data/processed/
ls results/

# Run update manually
python update_dashboard.py
```

**Analysis slow?**
- First run downloads 1 year of data (~1-2 min)
- Subsequent runs faster (incremental)
- Can reduce `days=365` in `main_analysis.py` to 90 for faster testing

---

## 📞 SUPPORT COMMANDS

**View all signals:**
```powershell
python main_analysis.py
```

**Update dashboard only:**
```powershell
python update_dashboard.py
```

**Run scheduler (automated):**
```powershell
python scheduler.py
```

**View current prices:**
```powershell
python -c "from src.data_loader import MarketDataLoader; m = MarketDataLoader(); m.print_available_assets()"
```

---

## 🎓 NEXT LEVEL

- Backtest strategy on more data
- Add more indicators (Stochastic, ATR bands)
- Implement trailing stops
- Create position sizing algorithm
- Add profit-taking levels

---

**Ready? Let's trade! 🚀**

1. Setup Telegram (TELEGRAM_SETUP.md)
2. Run first analysis: `python main_analysis.py`
3. Open dashboard: `dashboard.html`
4. Enable notifications: `python update_dashboard.py`
5. Start receiving daily Telegram alerts! 📱

---

Monitor your trades 24/7. Never miss a signal. Trade smart with data-driven decisions! 📊💹
