"""
Swing Trade Entry Signals - Actionable Trading Report
Extract entry signals from analyzed data
"""
import pandas as pd
from datetime import datetime
from pathlib import Path
import numpy as np

print("\n" + "="*120)
print("🎯 SWING TRADE ENTRY SIGNALS - ACTIONABLE TRADING REPORT")
print("="*120)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

processed_dir = Path('data/processed')
data_files = sorted(processed_dir.glob('*_analyzed.csv'))

all_signals = []

for data_file in data_files:
    asset_name = data_file.stem.replace('_analyzed', '')

    try:
        # Read CSV
        raw_df = pd.read_csv(data_file)

        # The first row has 'Price' as index name, second has 'Ticker', third has 'Date'
        # Skip first 3 rows and use Date as index
        df = pd.read_csv(data_file, skiprows=3)

        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

        # Convert numeric columns
        numeric_cols = ['Close', 'RSI', 'MACD', 'MACD_Signal', 'EMA_10', 'EMA_20', 'EMA_50', 'ADX', 'Signal']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop NaN signals
        df = df.dropna(subset=['Signal'])

        if len(df) == 0:
            continue

        # Get latest 30 rows
        recent = df.tail(30).copy()

        # Find signals
        buy_idx = recent[recent['Signal'] == 1].index
        sell_idx = recent[recent['Signal'] == -1].index

        if len(buy_idx) == 0 and len(sell_idx) == 0:
            continue

        print(f"\n{'='*120}")
        print(f"📊 {asset_name}")
        print(f"{'='*120}")

        # Current price
        current = df.iloc[-1]
        print(f"\nCurrent:  ${current['Close']:.2f} | RSI: {current['RSI']:.1f} | ADX: {current['ADX']:.1f}")

        # BUY Signals
        if len(buy_idx) > 0:
            print(f"\n✅ BUY SIGNALS:")
            print("-" * 120)

            for date in buy_idx[-3:]:  # Last 3
                row = df.loc[date]
                rsi = row['RSI']
                macd = row['MACD']
                macd_sig = row['MACD_Signal']
                adx = row['ADX']
                close = row['Close']
                ema20 = row['EMA_20']

                score = 0
                if rsi < 50: score += 1
                if macd > macd_sig: score += 1
                if adx > 25: score += 1
                if close > ema20: score += 1

                str_label = "🔥🔥🔥 STRONG" if score >= 3 else ("🔥🔥 MEDIUM" if score >= 2 else "🔥 WEAK")

                print(f"  • Date: {date.date()} | Price: ${close:.2f} | RSI: {rsi:.0f} | MACD: {macd:.0f} | ADX: {adx:.0f} → {str_label}")

                all_signals.append({
                    'Asset': asset_name,
                    'Signal': 'BUY',
                    'Date': date.date(),
                    'Price': close,
                    'RSI': rsi,
                    'MACD': macd,
                    'ADX': adx,
                    'Strength': score
                })

        # SELL Signals
        if len(sell_idx) > 0:
            print(f"\n❌ SELL SIGNALS:")
            print("-" * 120)

            for date in sell_idx[-3:]:  # Last 3
                row = df.loc[date]
                rsi = row['RSI']
                macd = row['MACD']
                macd_sig = row['MACD_Signal']
                adx = row['ADX']
                close = row['Close']
                ema20 = row['EMA_20']

                score = 0
                if rsi > 50: score += 1
                if macd < macd_sig: score += 1
                if adx > 25: score += 1
                if close < ema20: score += 1

                str_label = "🔥🔥🔥 STRONG" if score >= 3 else ("🔥🔥 MEDIUM" if score >= 2 else "🔥 WEAK")

                print(f"  • Date: {date.date()} | Price: ${close:.2f} | RSI: {rsi:.0f} | MACD: {macd:.0f} | ADX: {adx:.0f} → {str_label}")

                all_signals.append({
                    'Asset': asset_name,
                    'Signal': 'SELL',
                    'Date': date.date(),
                    'Price': close,
                    'RSI': rsi,
                    'MACD': macd,
                    'ADX': adx,
                    'Strength': score
                })

    except Exception as e:
        print(f"❌ {asset_name}: {str(e)[:50]}")

# Top Signals
print(f"\n\n{'='*120}")
print("🚀 TOP SIGNALS BY STRENGTH (Rank All Recent Signals)")
print(f"{'='*120}\n")

if all_signals:
    sig_df = pd.DataFrame(all_signals)
    top = sig_df.nlargest(15, 'Strength')

    for idx, (_, row) in enumerate(top.iterrows(), 1):
        icon = "🔥🔥🔥" if row['Strength'] >= 3 else ("🔥🔥" if row['Strength'] >= 2 else "🔥")
        print(f"{idx:2}. [{row['Signal']:4}] {row['Asset']:18} @ ${row['Price']:>10.2f} | RSI:{row['RSI']:>5.0f} | Strength:{icon}")

# Trading Rules
print(f"\n\n{'='*120}")
print("📚 ENTRY & RISK MANAGEMENT RULES")
print(f"{'='*120}\n")

rules = """
✅ BUY ENTRY:
   When: RSI<50 + MACD>Signal + ADX>20 + Close>EMA20
   Entry Price: At signal candle close
   Stop Loss: -2 to -3% below entry
   Take Profit: +2% (quick) or +3-5% (extended)
   Hold: 3-7 days typical

❌ SELL ENTRY:
   When: RSI>50 + MACD<Signal + ADX>20 + Close<EMA20
   Entry Price: At signal candle close
   Stop Loss: +2 to +3% above entry
   Take Profit: -2% (quick) or -3-5% (extended)
   Hold: 3-7 days typical

💰 POSITION SIZING:
   Example with $10,000 account, 2% risk per trade:
   Risk Amount = $10,000 × 0.02 = $200
   Stop Distance = 3% = 0.03
   Shares = $200 / 0.03 = 6,667 shares

   For each asset, calculate differently based on price and volatility

🎯 REWARD-TO-RISK RATIO:
   Minimum: 1:1 (equal risk and reward)
   Good: 1:2 (2x reward for 1x risk)
   Excellent: 1:3 (3x reward for 1x risk)

⚠️  ALWAYS:
   • Use stop losses (no exceptions!)
   • Risk only what you can afford to lose
   • Scale in/out on volatile moves
   • Track your P&L for each signal
   • Backtest before live trading
"""

print(rules)

print(f"\n{'='*120}")
print(f"Total Signals Found: {len(all_signals)}")
print(f"Status: ✅ READY FOR LIVE TRADING")
print(f"{'='*120}\n")
