"""
Bond Data Fetcher - Get US Treasury Yields Daily
Data sources: FRED, yfinance, Treasury Direct
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

print("\n" + "="*120)
print("💰 BOND DATA FETCHER - US TREASURY YIELDS & YIELD CURVE")
print("="*120)
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Try yfinance first (fastest)
print("Fetching bond yields from yfinance...\n")

bond_symbols = {
    '^IRX': '3-Month Bill',
    '^TYX': '2-Year Note',
    '^FVX': '5-Year Note',
    '^TNX': '10-Year Note (MAIN)',
    '^TXY': '30-Year Bond'
}

yields_data = {}
success_count = 0

for symbol, description in bond_symbols.items():
    try:
        data = yf.download(symbol, period='5d', progress=False)

        if len(data) > 0:
            latest_close = float(data['Close'].iloc[-1])
            yield_pct = latest_close / 100  # Convert basis points to percentage

            # Calculate change
            if len(data) > 1:
                prev_close = float(data['Close'].iloc[-2])
                change = latest_close - prev_close
            else:
                change = 0

            yields_data[description] = {
                'value': yield_pct,
                'basis_points': latest_close,
                'change': change,
                'symbol': symbol
            }

            status = "📈" if change > 0 else ("📉" if change < 0 else "➡️")
            print(f"✅ {description:25} | {yield_pct:6.3f}% ({latest_close:>7.2f} bps) | {status} {change:+.2f}")
            success_count += 1

    except Exception as e:
        print(f"❌ {description:25} | Error: {str(e)[:50]}")

print(f"\n✅ Successfully fetched: {success_count}/{len(bond_symbols)} yields\n")

# === YIELD CURVE ANALYSIS ===
if '10-Year Note (MAIN)' in yields_data and '2-Year Note' in yields_data:
    print("="*120)
    print("📊 YIELD CURVE ANALYSIS")
    print("="*120)

    y10 = yields_data['10-Year Note (MAIN)']['basis_points']
    y2 = yields_data['2-Year Note']['basis_points']
    spread_bps = y10 - y2

    print(f"\n10-Year Yield: {y10/100:6.3f}%")
    print(f"2-Year Yield:  {y2/100:6.3f}%")
    print(f"Spread (10Y-2Y): {spread_bps:+.1f} basis points")

    if spread_bps > 0:
        print(f"\n✅ CURVE STATUS: NORMAL (Healthy economy)")
        print(f"   Interpretation: Growth expectations, normal environment")
        print(f"   Trading Impact: Favor BUY signals, risk-on assets")
    elif spread_bps > -50:
        print(f"\n⚠️  CURVE STATUS: FLATTENING (Watch for inversion)")
        print(f"   Interpretation: Growth concerns emerging")
        print(f"   Trading Impact: Tighten stops, reduce position size")
    else:
        print(f"\n❌ CURVE STATUS: INVERTED (Recession signal!)")
        print(f"   Interpretation: Major recession warning")
        print(f"   Trading Impact: Avoid aggressive longs, favor shorts")

# === MACRO IMPACT ===
print(f"\n{'='*120}")
print("🌍 MACRO IMPACT ON TRADING SIGNALS")
print(f"{'='*120}\n")

if '10-Year Note (MAIN)' in yields_data:
    y10_change = yields_data['10-Year Note (MAIN)']['change']

    if y10_change > 5:
        scenario = "📈 YIELDS RISING SHARPLY"
        impact = """
Asset Impact:
  ❌ Gold: SELL (avoid longs)
  ❌ Oil: SELL (avoid longs)
  ❌ Stocks: CAUTION (lower valuations)
  ✅ USD Pairs: BUY (dollar strength)
  ⚠️  Bond Prices: FALLING

Trading Strategy:
  • Reduce commodity position sizes to 50%
  • Favor USD/JPY and GBP/USD BUYs
  • Avoid NASDAQ BUYs (growth stock risk)
  • Take oil/gold SELL signals
        """
    elif y10_change > 0:
        scenario = "📈 YIELDS RISING (MILD)"
        impact = """
Asset Impact:
  ⚠️  Gold: Mixed (watch closely)
  ⚠️  Oil: Mixed (watch closely)
  ➡️  Stocks: Neutral
  ✅ USD Pairs: Slight edge

Trading Strategy:
  • Normal position sizing
  • Monitor daily yield moves
  • Prefer higher-conviction signals
        """
    elif y10_change < -5:
        scenario = "📉 YIELDS FALLING SHARPLY"
        impact = """
Asset Impact:
  ✅ Gold: BUY (rally)
  ✅ Oil: BUY (rally)
  ✅ Stocks: STRONG BUY (rising valuations)
  ❌ USD Pairs: SELL (dollar weakness)
  ✅ Bond Prices: RISING

Trading Strategy:
  • Full position size on commodity BUYs
  • Take all NASDAQ/Bitcoin BUYs
  • Skip USD pair longs
  • Take USD pair SHORT signals
        """
    elif y10_change < 0:
        scenario = "📉 YIELDS FALLING (MILD)"
        impact = """
Asset Impact:
  ✅ Gold: Slight edge (buying)
  ✅ Oil: Slight edge (buying)
  ✅ Stocks: Positive
  ➡️  USD Pairs: Neutral

Trading Strategy:
  • Normal position sizing
  • Slight preference for risk-on trades
  • Commodities look better
        """
    else:
        scenario = "➡️ YIELDS STABLE"
        impact = """
Asset Impact:
  ➡️  All assets: Normal behavior
  ➡️  Correlations: Historical norms

Trading Strategy:
  • Use all signals equally
  • Standard position sizing
  • Follow technical setups
        """

    print(f"Current Scenario: {scenario}")
    print(f"10Y Change Today: {y10_change:+.2f} basis points")
    print(impact)

# === SAVE DATA ===
if yields_data:
    print(f"\n{'='*120}")
    print("💾 SAVING DATA")
    print(f"{'='*120}\n")

    # Create dataframe
    df_yields = pd.DataFrame([yields_data])
    df_yields.index = [datetime.now()]

    # Save/append to historical file
    filename = 'data/bond_yields_historical.csv'
    os.makedirs('data', exist_ok=True)

    if os.path.exists(filename):
        existing_df = pd.read_csv(filename, index_col=0, parse_dates=True)
        df_combined = pd.concat([existing_df, df_yields])
        df_combined.to_csv(filename)
        print(f"✅ Appended to: {filename}")
        print(f"   Total records: {len(df_combined)}")
    else:
        df_yields.to_csv(filename)
        print(f"✅ Created: {filename}")

# === SUMMARY ===
print(f"\n{'='*120}")
print("📋 SUMMARY & ACTION ITEMS")
print(f"{'='*120}\n")

summary = """
Key Bond Yields to Monitor Daily:

1. 10-Year Treasury Yield (^TNX)
   → Most important for macro analysis
   → Inverse correlation with gold, oil
   → Direct impact on equity valuations

2. 2-Year Treasury Yield (^TYX)
   → Use for yield curve (10Y-2Y spread)
   → Watch for inversion (recession warning)

3. 3-Month Bill Yield (^IRX)
   → Near-term Fed policy indicator
   → Money market barometer

Action Items:
✅ Bookmark: https://fred.stlouisfed.org/series/DGS10
✅ Add to portfolio watch: Yields 10Y, 2Y, 3M
✅ Check daily before trading
✅ Track 10Y-2Y spread
✅ Schedule daily automated fetch

Integration with Trading System:
→ High yields (>3.5%) + rising = Risk-off (trade defensively)
→ Low yields (<2.5%) + falling = Risk-on (trade aggressively)
→ Inverted curve (2Y > 10Y) = Recession warning (reduce position size 50%)
→ Normal curve (2Y < 10Y) = Health (full position sizing OK)
"""

print(summary)

print(f"{'='*120}")
print("✅ BOND DATA FETCH COMPLETE")
print(f"{'='*120}\n")

# Display data as table
print("\n" + "="*120)
print("📊 CURRENT YIELDS TABLE")
print("="*120 + "\n")

if yields_data:
    print(f"{'Instrument':<30} | {'Yield':<12} | {'Basis Points':<15} | {'Change (bps)':<15}")
    print("-" * 120)

    for desc, data in yields_data.items():
        yield_pct = data['value']
        bps = data['basis_points']
        change = data['change']

        status = "📈" if change > 0 else ("📉" if change < 0 else "➡️")
        print(f"{desc:<30} | {yield_pct:>10.3f}% | {bps:>13.2f} | {status} {change:>+12.2f}")

    print("\n" + "="*120)
