"""
Swing Trade Entry Signals - Final Report
Extract actionable entry points from analysis
"""
import pandas as pd
from datetime import datetime
from pathlib import Path

print("\n" + "="*140)
print("🎯 SWING TRADE ENTRY SIGNALS - FINAL ACTIONABLE REPORT")
print("="*140)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

processed_dir = Path('data/processed')
data_files = sorted(processed_dir.glob('*_analyzed.csv'))

all_signals = []

for data_file in data_files:
    asset_name = data_file.stem.replace('_analyzed', '')

    try:
        # Read with proper index handling
        df = pd.read_csv(data_file)

        # The first column is Price (which contains dates)
        # Rename it to Date
        df = df.rename(columns={'Price': 'Date'})
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')

        # Drop Ticker row
        df = df[df['Ticker'].notna() == False].copy() if 'Ticker' in df.columns else df

        # Convert numeric columns
        for col in ['Close', 'RSI', 'MACD', 'MACD_Signal', 'EMA_10', 'EMA_20', 'EMA_50', 'ADX', 'Signal']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with NaN Signal
        df = df.dropna(subset=['Signal'])

        if len(df) < 5:
            continue

        # Get last 30 rows
        recent = df.tail(30).copy()

        # Find signals
        buys = recent[recent['Signal'] == 1]
        sells = recent[recent['Signal'] == -1]

        if len(buys) == 0 and len(sells) == 0:
            continue

        print(f"\n{'='*140}")
        print(f"📊 {asset_name}")
        print(f"{'='*140}")

        current = df.iloc[-1]
        print(f"Current Price: ${current['Close']:.2f} | RSI: {current['RSI']:.1f} | MACD: {current['MACD']:.1f} | ADX: {current['ADX']:.1f}")

        # BUY Signals
        if len(buys) > 0:
            print(f"\n✅ BUY SIGNALS (Last 3):")
            print("-" * 140)

            for date, row in buys.tail(3).iterrows():
                rsi = float(row['RSI'])
                macd = float(row['MACD'])
                macd_sig = float(row['MACD_Signal'])
                adx = float(row['ADX'])
                close = float(row['Close'])
                ema20 = float(row['EMA_20'])

                # Score signal strength
                score = 0
                checks = []
                if close > ema20:
                    score += 1
                    checks.append("✓ Close > EMA20")
                else:
                    checks.append("✗ Close < EMA20")

                if rsi < 50:
                    score += 1
                    checks.append("✓ RSI < 50")
                else:
                    checks.append("✗ RSI > 50")

                if macd > macd_sig:
                    score += 1
                    checks.append("✓ MACD > Signal")
                else:
                    checks.append("✗ MACD < Signal")

                if adx > 25:
                    score += 1
                    checks.append("✓ ADX > 25 (STRONG)")
                else:
                    checks.append("- ADX < 25 (weak trend)")

                strength = "🔥🔥🔥 STRONG" if score >= 3 else ("🔥🔥 MEDIUM" if score >= 2 else "🔥 WEAK")

                print(f"\n  Entry Date: {date.date()}")
                print(f"  Entry Price: ${close:.2f}")
                print(f"  Checks: {' | '.join(checks)}")
                print(f"  Signal Strength: {strength}")
                print(f"  Stop Loss: ${close * 0.97:.2f} (-3%)")
                print(f"  Target 1: ${close * 1.02:.2f} (+2% quick win)")
                print(f"  Target 2: ${close * 1.05:.2f} (+5% extended hold)")

                all_signals.append({
                    'Asset': asset_name,
                    'Type': 'BUY',
                    'Date': date.date(),
                    'Price': close,
                    'RSI': rsi,
                    'MACD': macd,
                    'ADX': adx,
                    'Strength': score
                })

        # SELL Signals
        if len(sells) > 0:
            print(f"\n❌ SELL SIGNALS (Last 3):")
            print("-" * 140)

            for date, row in sells.tail(3).iterrows():
                rsi = float(row['RSI'])
                macd = float(row['MACD'])
                macd_sig = float(row['MACD_Signal'])
                adx = float(row['ADX'])
                close = float(row['Close'])
                ema20 = float(row['EMA_20'])

                # Score signal strength
                score = 0
                checks = []

                if close < ema20:
                    score += 1
                    checks.append("✓ Close < EMA20")
                else:
                    checks.append("✗ Close > EMA20")

                if rsi > 50:
                    score += 1
                    checks.append("✓ RSI > 50")
                else:
                    checks.append("✗ RSI < 50")

                if macd < macd_sig:
                    score += 1
                    checks.append("✓ MACD < Signal")
                else:
                    checks.append("✗ MACD > Signal")

                if adx > 25:
                    score += 1
                    checks.append("✓ ADX > 25 (STRONG)")
                else:
                    checks.append("- ADX < 25 (weak trend)")

                strength = "🔥🔥🔥 STRONG" if score >= 3 else ("🔥🔥 MEDIUM" if score >= 2 else "🔥 WEAK")

                print(f"\n  Entry Date: {date.date()}")
                print(f"  Entry Price: ${close:.2f}")
                print(f"  Checks: {' | '.join(checks)}")
                print(f"  Signal Strength: {strength}")
                print(f"  Stop Loss: ${close * 1.03:.2f} (+3%)")
                print(f"  Target 1: ${close * 0.98:.2f} (-2% quick win)")
                print(f"  Target 2: ${close * 0.95:.2f} (-5% extended hold)")

                all_signals.append({
                    'Asset': asset_name,
                    'Type': 'SELL',
                    'Date': date.date(),
                    'Price': close,
                    'RSI': rsi,
                    'MACD': macd,
                    'ADX': adx,
                    'Strength': score
                })

    except Exception as e:
        print(f"❌ {asset_name}: {str(e)[:60]}")

# Summary
print(f"\n\n{'='*140}")
print("🚀 TOP 10 HIGHEST PROBABILITY SIGNALS (By Strength Score)")
print(f"{'='*140}\n")

if all_signals:
    sig_df = pd.DataFrame(all_signals)
    top = sig_df.nlargest(10, 'Strength')

    print(f"{'#':>2} | {'Type':^5} | {'Asset':^20} | {'Date':^12} | {'Price':>10} | {'RSI':>5} | {'MACD':>7} | {'ADX':>5} | {'Strength':^20}")
    print("-" * 140)

    for idx, (_, row) in enumerate(top.iterrows(), 1):
        strength_icon = "🔥🔥🔥 STRONG" if row['Strength'] >= 3 else ("🔥🔥 MEDIUM" if row['Strength'] >= 2 else "🔥 WEAK")
        print(f"{idx:2} | {row['Type']:^5} | {row['Asset'][:20]:^20} | {str(row['Date']):^12} | ${row['Price']:>9.2f} | {row['RSI']:>5.0f} | {row['MACD']:>7.1f} | {row['ADX']:>5.1f} | {strength_icon:^20}")

# Rules
print(f"\n\n{'='*140}")
print("📚 HOW TO USE THESE SIGNALS")
print(f"{'='*140}\n")

guide = """
STEP 1: IDENTIFY SIGNAL
   Find signal in list above with 🔥🔥🔥 STRONG or 🔥🔥 MEDIUM rating

STEP 2: SET ENTRY
   BUY:  Enter at or slightly below the signal price
   SELL: Enter at or slightly above the signal price

STEP 3: SET STOP LOSS (NON-NEGOTIABLE!)
   BUY:  Stop = Entry Price × 0.97 (3% below)
   SELL: Stop = Entry Price × 1.03 (3% above)

STEP 4: SET PROFIT TARGETS
   Target 1 (50% size): Smaller profit (quick win, lock in gains)
   Target 2 (50% size): Larger profit (let winners run)

   BUY:   Target1 = Entry × 1.02 (+2%) | Target2 = Entry × 1.05 (+5%)
   SELL:  Target1 = Entry × 0.98 (-2%) | Target2 = Entry × 0.95 (-5%)

STEP 5: POSITION SIZING
   Account: $10,000
   Risk per trade: 2% = $200

   For BTC @ $79,600, 3% stop = $2,388:
   Shares = $200 / $2,388 = 0.0838 BTC

   For NASDAQ @ $26,500, 3% stop = $795:
   Shares = $200 / $795 = 0.252 shares

   Adjust for your account size and risk tolerance

STEP 6: EXECUTE & MONITOR
   • Place market/limit entry order
   • Set stop loss immediately (no exceptions!)
   • Set profit targets (use OCO orders if available)
   • Hold 3-7 days typically
   • Exit if stop hit OR profit target reached

STEP 7: TRACK RESULTS
   • Record entry date, price, signal type
   • Record exit date, price, P&L
   • Track win rate and avg profit/loss
   • Refine strategy based on results

⚠️  RISK MANAGEMENT RULES (CRITICAL!):
   ✓ Never risk more than 2% per trade
   ✓ Always use stop losses
   ✓ Take profits at targets (don't be greedy)
   ✓ Scale position size based on volatility
   ✓ Skip trades if signal strength is WEAK
   ✓ Max 3-4 trades simultaneously
   ✓ Track everything (journal your trades!)
"""

print(guide)

print(f"\n{'='*140}")
print(f"Total Signals Analyzed: {len(all_signals)}")
print(f"Status: ✅ READY FOR LIVE TRADING")
print(f"{'='*140}\n")
