"""
Comprehensive Swing Trade Entry Signals Report
Analyze all pairs and identify actionable entry points
"""
import pandas as pd
from datetime import datetime
from pathlib import Path

print("\n" + "="*120)
print("🎯 SWING TRADE ENTRY SIGNALS - ACTIONABLE TRADING REPORT")
print("="*120)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Read all analyzed data
processed_dir = Path('data/processed')
data_files = list(processed_dir.glob('*_analyzed.csv'))

all_entry_signals = []

print("Analyzing all market pairs...\n")

for data_file in sorted(data_files):
    asset_name = data_file.stem.replace('_analyzed', '')

    try:
        # Read with proper handling
        df = pd.read_csv(data_file, index_col='Date', parse_dates=True)

        # Skip header rows and clean data
        if 'Ticker' in df.index:
            df = df.drop('Ticker')

        # Convert columns to numeric
        for col in ['Close', 'RSI', 'MACD', 'MACD_Signal', 'EMA_10', 'EMA_20', 'EMA_50', 'ADX', 'Signal']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Remove rows with NaN signals
        df = df.dropna(subset=['Signal'])

        if len(df) == 0:
            continue

        # Get last 20 rows for analysis
        recent_df = df.tail(20)

        # Find BUY signals (Signal == 1)
        buy_signals = recent_df[recent_df['Signal'] == 1]

        # Find SELL signals (Signal == -1)
        sell_signals = recent_df[recent_df['Signal'] == -1]

        if len(buy_signals) > 0 or len(sell_signals) > 0:
            print(f"\n{'='*120}")
            print(f"📊 {asset_name}")
            print(f"{'='*120}")

            # Current price info
            current_row = df.iloc[-1]
            print(f"\nCurrent Price: ${current_row['Close']:.2f}")
            print(f"Current RSI: {current_row['RSI']:.2f} | ADX: {current_row['ADX']:.2f} | MACD: {current_row['MACD']:.2f}")

            # BUY SIGNALS
            if len(buy_signals) > 0:
                print(f"\n✅ BUY SIGNALS (Last 5):")
                print("-" * 120)

                for idx, (date, row) in enumerate(buy_signals.tail(5).iterrows(), 1):
                    rsi = float(row['RSI']) if pd.notna(row['RSI']) else 0
                    macd = float(row['MACD']) if pd.notna(row['MACD']) else 0
                    macd_signal = float(row['MACD_Signal']) if pd.notna(row['MACD_Signal']) else 0
                    adx = float(row['ADX']) if pd.notna(row['ADX']) else 0
                    close = float(row['Close'])
                    ema20 = float(row['EMA_20']) if pd.notna(row['EMA_20']) else 0

                    # Determine signal strength
                    strength_score = 0
                    if rsi < 50:
                        strength_score += 1
                    if macd > macd_signal:
                        strength_score += 1
                    if adx > 25:
                        strength_score += 1
                    if close > ema20:
                        strength_score += 1

                    strength = "🔥🔥🔥 STRONG" if strength_score >= 3 else ("🔥🔥 MEDIUM" if strength_score >= 2 else "🔥 WEAK")

                    print(f"\n  Entry #{idx}")
                    print(f"    Date:        {date.date()}")
                    print(f"    Entry Price: ${close:.2f}")
                    print(f"    RSI:         {rsi:.1f} (room to go up: {'YES' if rsi < 50 else 'NO'})")
                    print(f"    MACD:        {macd:.2f} vs Signal: {macd_signal:.2f} (bullish: {'YES' if macd > macd_signal else 'NO'})")
                    print(f"    ADX:         {adx:.1f} (trend strength: {'YES' if adx > 25 else 'NO'})")
                    print(f"    EMA20:       ${ema20:.2f} (above trend: {'YES' if close > ema20 else 'NO'})")
                    print(f"    Strength:    {strength}")

                    all_entry_signals.append({
                        'Asset': asset_name,
                        'Type': 'BUY',
                        'Date': date.date(),
                        'Price': close,
                        'RSI': rsi,
                        'MACD': macd,
                        'ADX': adx,
                        'Strength': strength_score,
                        'Status': 'ACTIVE' if idx == len(buy_signals) else 'PAST'
                    })

            # SELL SIGNALS
            if len(sell_signals) > 0:
                print(f"\n❌ SELL SIGNALS (Last 5):")
                print("-" * 120)

                for idx, (date, row) in enumerate(sell_signals.tail(5).iterrows(), 1):
                    rsi = float(row['RSI']) if pd.notna(row['RSI']) else 0
                    macd = float(row['MACD']) if pd.notna(row['MACD']) else 0
                    macd_signal = float(row['MACD_Signal']) if pd.notna(row['MACD_Signal']) else 0
                    adx = float(row['ADX']) if pd.notna(row['ADX']) else 0
                    close = float(row['Close'])
                    ema20 = float(row['EMA_20']) if pd.notna(row['EMA_20']) else 0

                    # Determine signal strength
                    strength_score = 0
                    if rsi > 50:
                        strength_score += 1
                    if macd < macd_signal:
                        strength_score += 1
                    if adx > 25:
                        strength_score += 1
                    if close < ema20:
                        strength_score += 1

                    strength = "🔥🔥🔥 STRONG" if strength_score >= 3 else ("🔥🔥 MEDIUM" if strength_score >= 2 else "🔥 WEAK")

                    print(f"\n  Entry #{idx}")
                    print(f"    Date:        {date.date()}")
                    print(f"    Entry Price: ${close:.2f}")
                    print(f"    RSI:         {rsi:.1f} (room to go down: {'YES' if rsi > 50 else 'NO'})")
                    print(f"    MACD:        {macd:.2f} vs Signal: {macd_signal:.2f} (bearish: {'YES' if macd < macd_signal else 'NO'})")
                    print(f"    ADX:         {adx:.1f} (trend strength: {'YES' if adx > 25 else 'NO'})")
                    print(f"    EMA20:       ${ema20:.2f} (below trend: {'YES' if close < ema20 else 'NO'})")
                    print(f"    Strength:    {strength}")

                    all_entry_signals.append({
                        'Asset': asset_name,
                        'Type': 'SELL',
                        'Date': date.date(),
                        'Price': close,
                        'RSI': rsi,
                        'MACD': macd,
                        'ADX': adx,
                        'Strength': strength_score,
                        'Status': 'ACTIVE' if idx == len(sell_signals) else 'PAST'
                    })

    except Exception as e:
        print(f"❌ Error reading {asset_name}: {str(e)[:100]}")

# Summary
print(f"\n\n{'='*120}")
print("📋 ENTRY SIGNALS SUMMARY TABLE")
print(f"{'='*120}\n")

if all_entry_signals:
    summary_df = pd.DataFrame(all_entry_signals)

    # Filter for ACTIVE signals only
    active_signals = summary_df[summary_df['Status'] == 'ACTIVE'].sort_values('Strength', ascending=False)

    if len(active_signals) > 0:
        print("🚀 MOST RECENT ACTIVE SIGNALS (Ranked by Strength):\n")
        for idx, (_, row) in enumerate(active_signals.head(15).iterrows(), 1):
            strength_icon = "🔥🔥🔥" if row['Strength'] >= 3 else ("🔥🔥" if row['Strength'] >= 2 else "🔥")
            print(f"{idx:2}. {row['Type']:4} │ {row['Asset']:20} │ ${row['Price']:>10.2f} │ RSI: {row['RSI']:>5.1f} │ Strength: {strength_icon}")

    print("\n" + "="*120)

# Trading Rules
print("\n" + "="*120)
print("📚 TRADING RULES & ENTRY STRATEGY")
print("="*120)

rules = """
ENTRY SIGNALS:

✅ BUY SIGNAL (Go LONG):
   Conditions:
   • Price > EMA20 (in uptrend)
   • RSI < 50 (room to go up)
   • MACD > Signal Line (bullish momentum)
   • ADX > 20 (trend strength)

   Entry: Buy at the signal price
   Stop Loss: 2-3% below entry
   Take Profit Target 1: +1.5-2% (quick win)
   Take Profit Target 2: +3-5% (longer hold)
   Holding Period: 3-7 days

❌ SELL SIGNAL (Go SHORT or EXIT):
   Conditions:
   • Price < EMA20 (in downtrend)
   • RSI > 50 (room to go down)
   • MACD < Signal Line (bearish momentum)
   • ADX > 20 (trend strength)

   Entry: Sell at the signal price
   Stop Loss: 2-3% above entry
   Take Profit Target 1: -1.5-2% (quick win)
   Take Profit Target 2: -3-5% (longer hold)
   Holding Period: 3-7 days

SIGNAL STRENGTH:
🔥🔥🔥 STRONG   (3-4 conditions met) - HIGH PROBABILITY, PREFERRED
🔥🔥  MEDIUM   (2 conditions met) - MEDIUM PROBABILITY, OK TO TRADE
🔥    WEAK     (1 condition met) - LOW PROBABILITY, AVOID OR USE SMALLER SIZE

RISK MANAGEMENT:
• Never risk more than 1-2% per trade
• Position sizing: (Risk Amount) / (Stop Loss Distance) = Shares
• Example: Risk $100 / 0.03 (3% stop) = 3,333 shares
• Profit target should be 1.5x - 3x your risk (1:1.5 to 1:3 reward:risk ratio)
"""

print(rules)

print("="*120)
print(f"\nReport generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Status: ✅ ALL SIGNALS ANALYZED AND READY FOR TRADING")
print("="*120 + "\n")
