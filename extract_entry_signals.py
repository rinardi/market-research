"""
Extract and analyze swing trade entry signals
Identify clear patterns for immediate trading
"""
import pandas as pd
import os
from pathlib import Path

print("\n" + "="*100)
print("SWING TRADE ENTRY SIGNALS ANALYSIS")
print("="*100)
print()

# Read all trade results
results_dir = Path('results')
trade_files = list(results_dir.glob('*_trades.csv'))

print(f"Found {len(trade_files)} trade result files\n")

signals_summary = []

for trade_file in sorted(trade_files):
    print("="*100)
    print(f"📊 {trade_file.stem}")
    print("="*100)

    try:
        df = pd.read_csv(trade_file, index_col=0, parse_dates=True)

        if df is None or len(df) == 0:
            print("❌ No data\n")
            continue

        # Filter for BUY signals (Signal == 1)
        buy_signals = df[df['Signal'] == 1].copy()

        # Filter for SELL signals (Signal == -1)
        sell_signals = df[df['Signal'] == -1].copy()

        print(f"Total rows analyzed: {len(df)}")
        print(f"BUY signals found: {len(buy_signals)}")
        print(f"SELL signals found: {len(sell_signals)}")
        print()

        if len(buy_signals) > 0:
            print("📈 RECENT BUY SIGNALS (Last 5):")
            print("-" * 100)

            recent_buys = buy_signals.tail(5)
            for idx, (date, row) in enumerate(recent_buys.iterrows(), 1):
                try:
                    print(f"\n  [{idx}] Date: {date.date() if hasattr(date, 'date') else date}")
                    print(f"      Price (Close): ${row['Close']:.2f}")
                    print(f"      RSI: {row.get('RSI', 'N/A')}")
                    print(f"      MACD: {row.get('MACD', 'N/A')}")
                    print(f"      EMA20: ${row.get('EMA_20', 'N/A')}")
                    print(f"      ADX: {row.get('ADX', 'N/A')}")
                    print(f"      Strength: {'STRONG' if row.get('ADX', 0) > 25 else 'WEAK'}")

                    signals_summary.append({
                        'Asset': trade_file.stem.replace('_trades', ''),
                        'Signal Type': 'BUY',
                        'Date': date,
                        'Price': row['Close'],
                        'RSI': row.get('RSI', None),
                        'MACD': row.get('MACD', None),
                        'ADX': row.get('ADX', None)
                    })
                except Exception as e:
                    print(f"      Error: {e}")

        if len(sell_signals) > 0:
            print("\n📉 RECENT SELL SIGNALS (Last 5):")
            print("-" * 100)

            recent_sells = sell_signals.tail(5)
            for idx, (date, row) in enumerate(recent_sells.iterrows(), 1):
                try:
                    print(f"\n  [{idx}] Date: {date.date() if hasattr(date, 'date') else date}")
                    print(f"      Price (Close): ${row['Close']:.2f}")
                    print(f"      RSI: {row.get('RSI', 'N/A')}")
                    print(f"      MACD: {row.get('MACD', 'N/A')}")
                    print(f"      EMA20: ${row.get('EMA_20', 'N/A')}")
                    print(f"      ADX: {row.get('ADX', 'N/A')}")
                    print(f"      Strength: {'STRONG' if row.get('ADX', 0) > 25 else 'WEAK'}")

                    signals_summary.append({
                        'Asset': trade_file.stem.replace('_trades', ''),
                        'Signal Type': 'SELL',
                        'Date': date,
                        'Price': row['Close'],
                        'RSI': row.get('RSI', None),
                        'MACD': row.get('MACD', None),
                        'ADX': row.get('ADX', None)
                    })
                except Exception as e:
                    print(f"      Error: {e}")

        print("\n")

    except Exception as e:
        print(f"❌ Error reading {trade_file.stem}: {e}\n")

# Summary table
print("\n" + "="*100)
print("QUICK ENTRY SIGNALS SUMMARY")
print("="*100)
print()

if signals_summary:
    summary_df = pd.DataFrame(signals_summary)
    print(summary_df.to_string(index=False))

print("\n" + "="*100)
print("LEGEND")
print("="*100)
print("""
BUY Signal:  Go LONG (buy and hold for 3-7 days)
SELL Signal: Go SHORT (or exit long position)

Entry Rules:
✅ RSI < 50 for BUY (room to go up)
✅ RSI > 50 for SELL (room to go down)
✅ MACD > Signal Line for BUY
✅ ADX > 20 for trend strength

Risk Management:
- Set stop loss 2-3% below entry
- Take profit at 1.5-3x risk/reward
- Risk only 1-2% per trade
""")

print("\n" + "="*100)
