"""
Swing Trade Entry Signals - FINAL REPORT
Extract all actionable entry signals from analyzed market data
"""
import pandas as pd
from pathlib import Path

print("\n" + "="*150)
print("🎯 SWING TRADE ENTRY SIGNALS - ACTIONABLE ENTRY POINTS")
print("="*150)

processed_dir = Path('data/processed')
data_files = sorted(processed_dir.glob('*_analyzed.csv'))

all_entries = []

for data_file in data_files:
    asset = data_file.stem.replace('_analyzed', '')

    df = pd.read_csv(data_file)

    # Skip first 2 rows (Ticker, Date headers)
    df = df.iloc[2:].reset_index(drop=True)
    df = df.rename(columns={'Price': 'Date'})

    # Convert Signal to numeric
    df['Signal'] = pd.to_numeric(df['Signal'], errors='coerce')

    # Find ALL buy and sell signals
    buys = df[df['Signal'] == 1.0]
    sells = df[df['Signal'] == -1.0]

    if len(buys) > 0:
        for idx, row in buys.iterrows():
            try:
                all_entries.append({
                    'Asset': asset,
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
                all_entries.append({
                    'Asset': asset,
                    'Type': 'SELL ❌',
                    'Date': row['Date'],
                    'Price': float(row['Close']),
                    'RSI': float(row['RSI']),
                    'MACD': float(row['MACD']),
                    'ADX': float(row['ADX']),
                })
            except:
                pass

if all_entries:
    result_df = pd.DataFrame(all_entries)

    print(f"\nTotal Entry Signals Found: {len(result_df)}\n")

    # Group by asset
    for asset in result_df['Asset'].unique():
        asset_signals = result_df[result_df['Asset'] == asset]
        print(f"\n{'='*150}")
        print(f"📊 {asset}")
        print(f"{'='*150}\n")
        print(f"{'Type':^8} | {'Date':^15} | {'Price':>12} | {'RSI':>6} | {'MACD':>8} | {'ADX':>6}")
        print("-" * 150)

        for _, row in asset_signals.iterrows():
            print(f"{row['Type']:^8} | {str(row['Date']):^15} | ${row['Price']:>11.2f} | {row['RSI']:>6.1f} | {row['MACD']:>8.1f} | {row['ADX']:>6.1f}")

    print(f"\n\n{'='*150}")
    print("📋 ALL SIGNALS SUMMARY TABLE")
    print(f"{'='*150}\n")

    # Sort by most recent
    result_df_sorted = result_df.sort_values('Date', ascending=False)

    print(f"{'#':>2} | {'Type':^8} | {'Asset':^18} | {'Date':^15} | {'Price':>12} | {'RSI':>6} | {'MACD':>8} | {'ADX':>6}")
    print("-" * 150)

    for idx, (_, row) in enumerate(result_df_sorted.iterrows(), 1):
        print(f"{idx:2} | {row['Type']:^8} | {str(row['Asset'])[:18]:^18} | {str(row['Date']):^15} | ${row['Price']:>11.2f} | {row['RSI']:>6.1f} | {row['MACD']:>8.1f} | {row['ADX']:>6.1f}")

    print(f"\n{'='*150}")
    print("✅ ENTRY SIGNAL GUIDE")
    print(f"{'='*150}\n")

    guide = """
SIGNAL TYPES:
✅ BUY  - Enter LONG (buy position, hold 3-7 days)
❌ SELL - Enter SHORT or exit LONG (short position or close buy)

ENTRY EXECUTION:
1. Identify signal from list above
2. Enter at the signal price (or 0.5% better if market allows)
3. Set STOP LOSS immediately (non-negotiable!)
   - BUY:  Stop = Price × 0.97 (-3%)
   - SELL: Stop = Price × 1.03 (+3%)
4. Set PROFIT TARGETS:
   - BUY:  Target1 = Price × 1.02 (+2%) | Target2 = Price × 1.05 (+5%)
   - SELL: Target1 = Price × 0.98 (-2%) | Target2 = Price × 0.95 (-5%)
5. Exit when target hit OR stop hit (whichever first)

RISK MANAGEMENT:
• Risk only 1-2% per trade
• Position Size = (Account × Risk%) / (Stop Loss Distance)
• Example: ($10,000 × 0.02) / 0.03 = $6,667 risk amount
• Reward must be 1.5x - 3x your risk
• Never stack more than 3-4 open positions

INDICATORS USED:
RSI < 50 for BUY (room to go up)
RSI > 50 for SELL (room to go down)
MACD > Signal for BUY (bullish)
MACD < Signal for SELL (bearish)
ADX > 20+ for trend strength confirmation
"""

    print(guide)

else:
    print("❌ No signals found in data")

print(f"{'='*150}\n")
