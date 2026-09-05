# Telegram Notifications Setup Guide

Monitor your swing trading analysis in real-time! Get instant alerts on your phone via Telegram.

---

## STEP 1: Create Telegram Bot

### 1.1 Get Bot Token from @BotFather

1. Open Telegram and find **@BotFather**
2. Send `/start` and follow the menu
3. Click **"Create a new bot"**
4. Name your bot (e.g., "SwingTradingBot")
5. BotFather will give you a **token** like:
   ```
   123456789:ABCdefGHIjklmnoPQRstuvWXYZ
   ```
6. **Copy and save this token** - you'll need it next

### 1.2 Get Your Chat ID

1. Open Telegram and find **@userinfobot**
2. Send `/start` - it will show your **User ID** (e.g., 987654321)
3. **Copy and save this ID** - you'll need it next

---

## STEP 2: Configure Environment Variables

### 2.1 Create .env File

1. Go to `D:\market-research\`
2. Copy `.env.example` to `.env`
3. Edit `.env` with your credentials:

```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklmnoPQRstuvWXYZ
TELEGRAM_CHAT_ID=987654321
```

### 2.2 Verify File Location

```
D:\market-research\.env
```

---

## STEP 3: Install Python Package

```powershell
D:\hpc-env\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## STEP 4: Test Telegram Connection

```powershell
D:\hpc-env\Scripts\Activate.ps1
python src/notifier.py
```

**Expected output:**
```
[OK] Sending test summary...
[OK] Sending test trade alert...
```

If successful, check your Telegram for test messages!

---

## USAGE OPTIONS

### Option A: Manual Daily Updates

Run analysis and send notifications manually:

```powershell
D:\hpc-env\Scripts\Activate.ps1
python main_analysis.py
python update_dashboard.py
```

### Option B: Automated Daily Scheduler

Run analysis and updates automatically every day:

```powershell
D:\hpc-env\Scripts\Activate.ps1
python scheduler.py
```

**Scheduled Times:**
- 09:00 AM - Primary analysis
- 05:00 PM - Secondary analysis

Press `Ctrl+C` to stop scheduler.

### Option C: Windows Task Scheduler (Recommended for 24/7 Monitoring)

Schedule daily automated runs:

1. Open **Task Scheduler**
2. Create New Task:
   - Name: `SwingTradingAnalysis`
   - Trigger: Daily at 09:00 AM
   - Action: Run script

3. Script content (save as `run_daily.bat`):
   ```batch
   @echo off
   cd D:\market-research
   D:\hpc-env\Scripts\Activate.ps1 -ExecutionPolicy Bypass
   python main_analysis.py
   python update_dashboard.py
   ```

---

## VIEW DASHBOARD

After running analysis:

1. Open `D:\market-research\dashboard.html` in your browser
2. View real-time market data:
   - Current prices
   - Returns %
   - Win rates
   - Trade signals (BUY/SELL/HOLD)

The dashboard updates automatically when you run `update_dashboard.py`

---

## TELEGRAM NOTIFICATIONS

### Market Summary

Receive daily summary of all markets:
- Stock Indices performance
- Commodities prices
- Forex pairs movements
- Crypto updates

Example:
```
SWING TRADING MONITOR
2026-09-04 09:00:00

TODAY HIGHLIGHTS:
Top: Oil WTI +46.31%
Bottom: Bitcoin -12.04%

INDICES:
📈 ^IXIC: +19.81% [BUY]
📈 ^GSPC: +14.79% [SELL]
📈 ^DJI: +12.40% [SELL]

[...more markets...]
```

### Trade Alerts

Instant notifications for new signals:

**BUY Signal Example:**
```
🟢 TRADE SIGNAL: BUY

Market: NASDAQ-100
Price: $22,017.85
Time: 09:30:45

Indicators:
RSI: 35.5
MACD: -150.23
EMA20: 6,500.00
ADX: 28.5

Action: BUY
Risk: 1-2% of capital
```

**SELL Signal Example:**
```
🔴 TRADE SIGNAL: SELL

Market: S&P 500
Price: $6,616.85
Time: 15:45:30

Indicators:
RSI: 72.3
MACD: 45.67
EMA20: 6,550.00
ADX: 32.1

Action: SELL
Risk: 1-2% of capital
```

---

## TROUBLESHOOTING

### No Telegram messages received?

1. **Check .env file:**
   ```powershell
   cat .env
   ```

2. **Verify token and chat ID are correct**
   - Token should have format: `123456789:ABC...`
   - Chat ID should be numeric

3. **Test bot directly:**
   ```powershell
   python src/notifier.py
   ```

4. **Check Telegram privacy settings:**
   - Bot should have permission to send messages
   - Make sure you started the bot with `/start`

### Analysis running but no notifications?

1. Ensure `.env` file exists with valid credentials
2. Run `python src/notifier.py` to test
3. Check `requirements.txt` - must have `requests` package

### Dashboard not updating?

1. Make sure CSV files exist:
   ```powershell
   ls results/
   ls data/processed/
   ```

2. Run `update_dashboard.py` separately:
   ```powershell
   python update_dashboard.py
   ```

---

## NEXT STEPS

1. **Setup Telegram notifications** (this guide)
2. **Run daily analysis:**
   ```powershell
   python main_analysis.py
   ```
3. **Update dashboard and send alerts:**
   ```powershell
   python update_dashboard.py
   ```
4. **Schedule automated runs** (optional):
   ```powershell
   python scheduler.py
   ```

---

## SECURITY NOTES

- **Never share your .env file** - it contains sensitive tokens
- Keep `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` private
- Add `.env` to `.gitignore` if using version control

```
# .gitignore
.env
*.pyc
__pycache__/
```

---

## SUPPORT

Having issues? Check:
1. Python is properly installed
2. Virtual environment is activated
3. `.env` file has correct credentials
4. Telegram bot is running (`/start` command sent)
5. All dependencies installed: `pip install -r requirements.txt`

---

Happy trading! Monitor your swing trades 24/7 via Telegram notifications!
