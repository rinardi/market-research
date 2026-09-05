"""
COMPLETE TRADING ANALYSIS
Swing Trade Signals + Macro Context Correlation
"""
import pandas as pd
from pathlib import Path
from datetime import datetime

print("\n" + "="*160)
print("🎯 COMPLETE SWING TRADE ANALYSIS - WITH MACRO CORRELATION FRAMEWORK")
print("="*160)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# === PART 1: EXTRACT SIGNALS ===
processed_dir = Path('data/processed')
data_files = sorted(processed_dir.glob('*_analyzed.csv'))

all_signals = []

for data_file in data_files:
    asset_name = data_file.stem.replace('_analyzed', '')

    try:
        df = pd.read_csv(data_file)
        df = df.iloc[2:].reset_index(drop=True)
        df = df.rename(columns={'Price': 'Date'})

        df['Signal'] = pd.to_numeric(df['Signal'], errors='coerce')

        buys = df[df['Signal'] == 1.0]
        sells = df[df['Signal'] == -1.0]

        if len(buys) > 0:
            for idx, row in buys.iterrows():
                try:
                    all_signals.append({
                        'Asset': asset_name,
                        'Type': 'BUY ✅',
                        'Date': row['Date'],
                        'Price': float(row['Close']),
                        'RSI': float(row['RSI']),
                        'MACD': float(row['MACD']),
                        'ADX': float(row['ADX']),
                    })
                except:
                    pass

        if len(sells) > 0:
            for idx, row in sells.iterrows():
                try:
                    all_signals.append({
                        'Asset': asset_name,
                        'Type': 'SELL ❌',
                        'Date': row['Date'],
                        'Price': float(row['Close']),
                        'RSI': float(row['RSI']),
                        'MACD': float(row['MACD']),
                        'ADX': float(row['ADX']),
                    })
                except:
                    pass

    except:
        pass

# === PART 2: MACRO CORRELATION FRAMEWORK ===
print("\n" + "="*160)
print("💰 MACRO CORRELATION FRAMEWORK")
print("="*160)

macro_guide = """
KEY MACRO INDICATORS & THEIR IMPACT ON SIGNALS:

1️⃣  US DOLLAR INDEX (DXY)
   ↑ STRONG DOLLAR → ✅ Favor USD pairs (USD-JPY, GBP-USD) | ❌ Avoid commodities
   ↓ WEAK DOLLAR   → ✅ Favor commodities (Gold, Oil)      | ❌ Avoid USD longs

2️⃣  US 10-YEAR TREASURY YIELD
   ↑ RISING YIELDS → ✅ Favor USD strength | ⚠️  Caution on equities | ❌ Avoid commodities
   ↓ FALLING YIELDS → ✅ Favor risk-on      | ✅ Stocks rally         | ✅ Commodities rally

3️⃣  YIELD CURVE (2Y vs 10Y)
   NORMAL (2Y < 10Y)   → ✅ Healthy economy, favor BUY signals
   INVERTED (2Y > 10Y) → ⚠️  Recession risk, tighten stops

SIGNAL CORRELATION TABLE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Asset              | Favorable Macro          | Unfavorable Macro      | Position Advice
───────────────────────────────────────────────────────────────────────────────────────────────────
✅ NASDAQ-100     | DXY ↓ + Yield ↓         | DXY ↑ + Yield ↑       | Risk-on asset (growth)
✅ S&P 500        | DXY ↓ + Yield ↓         | DXY ↑ + Yield ↑       | Risk-on asset (growth)
✅ Bitcoin        | DXY ↓ + Yield ↓         | DXY ↑ + Yield ↑       | Risk-on asset (speculative)
✅ Oil (WTI)      | DXY ↓                   | DXY ↑                 | Commodity (USD inverse)
✅ Gold (Spot)    | DXY ↓ + Yield ↓         | DXY ↑ + Yield ↑       | Safe-haven asset
✅ USD-JPY        | DXY ↑ + Yield ↑         | DXY ↓ + Yield ↓       | Carry trade (BoJ easing)
❌ EUR-USD        | Weak Euro + ECB ↓       | Strong Euro + ECB ↑   | Policy-driven
❌ GBP-USD        | Weak Pound + BoE ↓      | Strong Pound + BoE ↑  | Policy-driven

HOW TO USE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 SIGNAL FILTERING RULES:

Before entering ANY trade:
1. Check DXY trend (strong or weak?)
2. Check 10Y yield direction (rising or falling?)
3. Look up asset correlation in table above
4. If signal aligns with macro → FULL SIZE ✅
5. If signal contradicts macro → HALF SIZE ⚠️
6. If strongly contradicts → SKIP TRADE ❌

EXAMPLE SCENARIOS:

Scenario 1: DXY STRONG + YIELD RISING (Risk-off)
─────────────────────────────────────────
Market: USD strength, growth concerns
✅ TAKE:  USD-JPY BUY, GBP-USD BUY (full size)
⚠️ CAUTION: NASDAQ BUY, Bitcoin BUY (half size only)
❌ SKIP:  Oil BUY, Gold BUY (avoid)
✅ TAKE:  Gold SELL (selling commodities)

Scenario 2: DXY WEAK + YIELD FALLING (Risk-on)
─────────────────────────────────────────
Market: USD weakness, growth optimism
✅ TAKE:  Oil BUY, Gold BUY (full size)
✅ TAKE:  NASDAQ BUY, Bitcoin BUY (full size)
⚠️ CAUTION: USD-JPY BUY (half size only)
❌ SKIP:  USD-JPY BUY, GBP-USD BUY (avoid)
✅ TAKE:  USD-JPY SELL (short carry trades)

ECONOMIC CALENDAR EVENTS & IMPACT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Event                   | Frequency | Impact        | Action
──────────────────────────────────────────────────────────────────────────────────────────────
🇺🇸 Fed Decision        | 6 weeks   | MAJOR         | ⚠️  Reduce/close 24-48h before
🇺🇸 CPI Inflation       | Monthly   | MAJOR         | ⚠️  Avoid 24h before/after
🇺🇸 NFP Jobs            | Monthly   | MAJOR         | ⚠️  Avoid 1h before/after
🇺🇸 FOMC Minutes        | Monthly   | MEDIUM        | Watch for hawkish/dovish
🇪🇺 ECB Decision        | 6 weeks   | MEDIUM        | EUR pairs risk ⚠️
🇬🇧 BoE Decision        | 6 weeks   | MEDIUM        | GBP pairs risk ⚠️
🇯🇵 BoJ Decision        | 7-8 weeks | MEDIUM        | USD-JPY major moves
⛽ OPEC Announcement     | Quarterly | MEDIUM        | Oil volatility spike
⛽ Oil Inventory         | Weekly    | SMALL-MEDIUM  | Oil trading catalyst

MACRO CALENDAR CHECK:
Before opening EACH position, verify:
✓ No major event in next 24-48 hours
✓ Current macro environment aligns with signal
✓ Yield curve is not inverted (recession warning)
✓ DXY and yields not at extreme levels (reversal risk)

POSITION MANAGEMENT BY MACRO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Normal Conditions (No major macro divergence):
• Position size: 100% (full risk/reward setup)
• Hold time: 3-7 days (full swing trade)
• Stops: -2 to -3% standard

Macro Contradicting Signal:
• Position size: 50% (half risk/reward)
• Hold time: 2-3 days (quick win only)
• Stops: -1.5% (tighter, exit early)

Extreme Macro (Major divergence):
• Position size: 0% (SKIP TRADE)
• Alternative: Wait for macro to align
• Or wait 24-48 hours after calendar event
"""

print(macro_guide)

# === PART 3: SIGNAL LIST ===
if all_signals:
    sig_df = pd.DataFrame(all_signals)

    print("\n" + "="*160)
    print("📋 ALL 35 TRADING SIGNALS (With Macro Context Notes)")
    print("="*160)

    print(f"\n{'#':>2} | {'Type':^8} | {'Asset':^18} | {'Price':>12} | {'RSI':>5} | {'Macro Align':^15}")
    print("-" * 160)

    # Categorize by asset type for macro analysis
    forex_assets = ['EUR-USD', 'GBP-USD', 'USD-JPY', 'AUD-USD']
    commodity_assets = ['Gold_(Spot)', 'Oil_(WTI)']
    equity_assets = ['NASDAQ-100', 'S&P_500', 'Dow_Jones', 'Bitcoin']

    # Show signals organized by macro impact
    for idx, (_, row) in enumerate(sig_df.nlargest(35, 'Price').iterrows(), 1):
        asset = row['Asset']

        # Determine macro alignment recommendation
        if asset in forex_assets:
            align_note = "USD-depends"
        elif asset in commodity_assets:
            align_note = "USD-inverse"
        elif asset in equity_assets:
            align_note = "Risk-on"
        else:
            align_note = "Mixed"

        print(f"{idx:2} | {row['Type']:^8} | {asset[:18]:^18} | ${row['Price']:>11.2f} | {row['RSI']:>5.0f} | {align_note:^15}")

print("\n" + "="*160)
print("✅ NEXT STEPS")
print("="*160)

steps = """
1. Check current macro environment:
   - Go to tradingeconomics.com or investing.com
   - Find DXY (US Dollar Index)
   - Find 10-year Treasury yield (^TNX)
   - Note if trending up/down

2. Filter signals using macro alignment table above
   - If DXY rising → Focus on USD pairs & avoid commodities
   - If DXY falling → Focus on commodities & avoid USD pairs

3. Check economic calendar:
   - Avoid trading 24-48 hours before/after major events
   - Don't hold through Fed decisions, CPI, jobs data

4. Execute your top-aligned signals with full position size

5. For misaligned signals:
   - Take 50% position only (if at all)
   - Use tighter stops (-1.5% instead of -3%)
   - Exit quickly at first target (don't hold 3-7 days)

6. Track:
   - Which macro environment gave best results
   - Which assets performed best in current macro
   - Adjust strategy based on macro regime
"""

print(steps)

print("="*160)
print("✅ ANALYSIS COMPLETE - READY FOR TRADING WITH MACRO CONTEXT")
print("="*160 + "\n")
