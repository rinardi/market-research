"""
Macro Context for Trading Signals
DXY (Dollar Index) + US Treasury Yield analysis
Shows correlation with entry signals
"""
import yfinance as yf
from datetime import datetime

print("\n" + "="*150)
print("💰 MACRO CONTEXT - CORRELATION ANALYSIS")
print("="*150)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Fetch DXY (US Dollar Index) - try alternative symbols
print("Fetching macro data...")
dxy_latest = dxy_change = None
dxy_status = "❌ No data"

for dxy_symbol in ['^DXY', 'DXY=F', 'DXDUSD=X']:
    try:
        dxy = yf.download(dxy_symbol, period='5d', progress=False)
        if len(dxy) > 0:
            dxy_latest = float(dxy['Close'].iloc[-1])
            dxy_prev = float(dxy['Close'].iloc[-2]) if len(dxy) > 1 else dxy_latest
            dxy_change = ((dxy_latest - dxy_prev) / dxy_prev) * 100 if dxy_prev != 0 else 0
            dxy_status = "📈 STRONG USD" if dxy_change > 0.5 else ("📉 WEAK USD" if dxy_change < -0.5 else "➡️ NEUTRAL")
            break
    except:
        continue

# Fetch US 10-Year Yield (using ^TNX symbol)
yield_latest = yield_change = None
yield_status = "❌ No data"

try:
    yield_10y = yf.download('^TNX', period='5d', progress=False)
    if len(yield_10y) > 0:
        val = yield_10y['Close'].iloc[-1]
        if isinstance(val, (int, float)):
            yield_latest = float(val) / 100  # Convert to percentage
            if len(yield_10y) > 1:
                val_prev = yield_10y['Close'].iloc[-2]
                if isinstance(val_prev, (int, float)):
                    yield_prev = float(val_prev) / 100
                    yield_change = (yield_latest - yield_prev) * 100  # basis points
                    yield_status = "📈 RISING" if yield_change > 5 else ("📉 FALLING" if yield_change < -5 else "➡️ STABLE")
            else:
                yield_status = "✅ DATA"
except Exception as e:
    pass

# Fetch 2-Year Yield for comparison
yield2_latest = None
try:
    yield_2y = yf.download('^IRX', period='5d', progress=False)
    if len(yield_2y) > 0:
        val = yield_2y['Close'].iloc[-1]
        if isinstance(val, (int, float)):
            yield2_latest = float(val) / 100
except Exception as e:
    pass

print("\n" + "="*150)
print("📊 CURRENT MACRO INDICATORS")
print("="*150)

if dxy_latest is not None:
    print(f"\n💵 US DOLLAR INDEX (DXY)")
    print(f"   Current: {dxy_latest:.2f}")
    print(f"   Change: {dxy_change:+.2f}%")
    print(f"   Status: {dxy_status}")
else:
    print(f"\n💵 US DOLLAR INDEX (DXY)")
    print(f"   Status: {dxy_status}")

if yield_latest is not None:
    print(f"\n📈 US 10-YEAR TREASURY YIELD")
    print(f"   Current: {yield_latest:.3f}% ({yield_latest*100:.1f} bps)")
    print(f"   Change: {yield_change:+.1f} bps")
    print(f"   Status: {yield_status}")
    if yield2_latest:
        print(f"\n📊 YIELD CURVE")
        print(f"   2-Year Yield: {yield2_latest:.3f}%")
        print(f"   10-Year Yield: {yield_latest:.3f}%")
        curve_spread = (yield_latest - yield2_latest) * 100
        print(f"   Spread (2-10Y): {curve_spread:+.1f} bps")
        curve_status = "✅ NORMAL" if curve_spread > 0 else "⚠️  INVERTED"
        print(f"   Curve Status: {curve_status}")
else:
    print(f"\n📈 US 10-YEAR TREASURY YIELD")
    print(f"   Status: {yield_status}")

print("\n" + "="*150)
print("🔗 CORRELATION IMPACT ON TRADING SIGNALS")
print("="*150)

correlations = """
STRONG USD (DXY Rising) + HIGH YIELDS (Rising 10Y):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Impact:
✅ USD-JPY, GBP-USD: BULLISH (dollar strength)
❌ Gold, Oil: BEARISH (higher USD = lower commodity prices)
❌ Emerging Markets: Risk-off environment
⚠️  Stocks: Mixed (higher rates = lower valuations)

Trading Strategy:
• Focus on USD-related BUY signals (carry trades)
• Avoid commodity shorts when yields rising
• Monitor equity exposure (higher rates headwind)

WEAK USD (DXY Falling) + LOW YIELDS (Falling 10Y):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Impact:
❌ USD-JPY, GBP-USD: BEARISH (dollar weakness)
✅ Gold, Oil: BULLISH (lower USD = higher commodity prices)
✅ Emerging Markets: Risk-on environment
✅ Stocks: Potential rally (lower rates = higher valuations)

Trading Strategy:
• Focus on commodity BUY signals (oil, gold)
• Avoid USD longs
• Favor risk-on trades (emerging markets, growth)

YIELD CURVE NORMAL (2Y < 10Y):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Healthy economic environment
✅ Banks profitable (positive carry)
✅ Favor equity BUY signals
✅ Risk-on sentiment

YIELD CURVE INVERTED (2Y > 10Y):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Recession warning signal
⚠️  Banks face margin squeeze
❌ Avoid aggressive longs
✅ Consider defensive positions

SIGNAL QUALITY BY MACRO ENVIRONMENT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Asset              | DXY Rising | DXY Falling | High Yield | Low Yield | Signal Quality
─────────────────────────────────────────────────────────────────────────────────────────────
✅ NASDAQ-100     | ⚠️  Neutral| ✅ STRONG  | ⚠️  Caution| ✅ STRONG | Favor Low Yield
✅ S&P 500        | ⚠️  Neutral| ✅ STRONG  | ⚠️  Caution| ✅ STRONG | Favor Low Yield
✅ Bitcoin        | ⚠️  Neutral| ✅ STRONG  | ⚠️  Caution| ✅ STRONG | Risk-on trades
✅ Oil (WTI)      | ❌ WEAK   | ✅ STRONG  | ❌ WEAK    | ✅ STRONG | Favor Weak USD
✅ Gold (Spot)    | ❌ WEAK   | ✅ STRONG  | ❌ WEAK    | ✅ STRONG | Favor Weak USD
✅ USD-JPY        | ✅ STRONG | ❌ WEAK    | ✅ STRONG  | ❌ WEAK   | Favor Strong USD
❌ EUR-USD        | ✅ STRONG | ❌ WEAK    | Mixed     | Mixed     | Watch ECB policy
❌ GBP-USD        | ✅ STRONG | ❌ WEAK    | Mixed     | Mixed     | Watch BoE policy

HOW TO USE THIS CONTEXT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. CHECK MACRO ENVIRONMENT FIRST
   If DXY strong + yields high → Risk-off → Avoid commodity longs, favor USD longs
   If DXY weak + yields low → Risk-on → Favor commodity longs, avoid USD longs

2. FILTER SIGNALS BY MACRO
   If market contradicts macro trend, reduce position size or skip trade
   If signal aligns with macro, increase position size (higher conviction)

3. WATCH FOR REVERSALS
   When macro trend changes (DXY turning down, yields plunging) → Expect signal reversals
   Tighten stops before macro data releases (Fed decisions, inflation data)

4. COMBINE WITH TECHNICAL
   Technical BUY + Macro Support = HIGH PROBABILITY ✅
   Technical BUY + Macro Against = LOW PROBABILITY ⚠️
"""

print(correlations)

print("\n" + "="*150)
print("📌 KEY ECONOMIC CALENDAR EVENTS (Impact on Macro)")
print("="*150)

calendar = """
FED DECISION (Every 6 weeks):
   → Impacts Treasury yields → Changes DXY
   → Effect on ALL signals (major reversal risk)
   ⚠️  AVOID trading 24-48 hours before/after

INFLATION DATA (CPI Monthly):
   → Impacts Fed expectations → Yields rise/fall
   → Strong inflation = higher yields = USD up
   ⚠️  Expect volatility on CPI release days

EMPLOYMENT DATA (First Friday monthly):
   → Impacts growth expectations
   → Strong jobs = higher yields = USD up
   ⚠️  Major swing trade opportunities around jobs day

OIL INVENTORY (Weekly):
   → Impacts Oil prices directly
   → OPEC announcements = Oil swings 2-5%
   ⚠️  Important for Oil (WTI) signals

CENTRAL BANK MEETINGS:
   ECB, BoE, BoJ, RBNZ → Currency-specific impacts
   ⚠️  Watch before Forex signals (EUR-USD, GBP-USD, USD-JPY)
"""

print(calendar)

print("\n" + "="*150)
print("✅ MACRO CONTEXT SUMMARY")
print("="*150)

if dxy_latest is not None and yield_latest is not None:
    print(f"\nCurrent Environment:")
    print(f"• DXY: {dxy_latest:.2f} ({dxy_change:+.2f}%) → {dxy_status}")
    print(f"• 10Y Yield: {yield_latest:.3f}% ({yield_change:+.1f} bps) → {yield_status}")

    if dxy_change > 0.5 and yield_change > 5:
        environment = "🔴 RISK-OFF: Avoid commodity longs, favor USD pairs, reduce equity positions"
    elif dxy_change < -0.5 and yield_change < -5:
        environment = "🟢 RISK-ON: Favor commodities, avoid USD longs, equity BUYs strong"
    elif dxy_change > 0.5:
        environment = "🟡 MIXED: DXY strong but yields stable - selective trading"
    elif yield_change > 5:
        environment = "🟡 MIXED: Yields rising but USD stable - bond impact"
    else:
        environment = "🟢 NEUTRAL: Normal market - proceed with technical signals"

    print(f"\n{environment}")
    print(f"\nRecommendation:")
    print(f"✅ Use macro context to FILTER signals (avoid anti-correlated trades)")
    print(f"✅ Increase size on macro-aligned signals")
    print(f"⚠️  Reduce size on contradictory signals")
    print(f"✅ Check before opening positions (always verify macro alignment)")

print(f"\n{'='*150}\n")
