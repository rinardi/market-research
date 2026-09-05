"""Get real-time current prices for Gold, Bitcoin, NASDAQ"""
import yfinance as yf
from datetime import datetime

print("\n" + "="*80)
print("REAL-TIME MARKET PRICES - TODAY")
print("="*80)
print("Timestamp: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")

assets = [
    ('Gold (GC=F)', 'GC=F'),
    ('Bitcoin (BTC-USD)', 'BTC-USD'),
    ('NASDAQ-100 (^IXIC)', '^IXIC')
]

results = []

for name, symbol in assets:
    try:
        # Fetch latest data
        data = yf.download(symbol, period='5d', progress=False)

        if data is None or len(data) == 0:
            print("❌ No data for " + name)
            continue

        # Handle MultiIndex columns from yfinance
        if len(data) > 0:
            latest_idx = len(data) - 1
            latest = data.iloc[latest_idx]

            # Extract values - handle both single and multi-column formats
            if isinstance(latest['Close'], float):
                close = latest['Close']
                high = latest['High']
                low = latest['Low']
                open_price = latest['Open']
                volume = int(latest['Volume'])
            else:
                # MultiIndex case - get first (only) value
                close = float(latest['Close'].iloc[0])
                high = float(latest['High'].iloc[0])
                low = float(latest['Low'].iloc[0])
                open_price = float(latest['Open'].iloc[0])
                volume = int(latest['Volume'].iloc[0])

            # Calculate change with previous day
            if len(data) >= 2:
                prev_latest = data.iloc[latest_idx - 1]
                if isinstance(prev_latest['Close'], float):
                    prev_close = prev_latest['Close']
                else:
                    prev_close = float(prev_latest['Close'].iloc[0])
                change = close - prev_close
                change_pct = (change / prev_close) * 100
            else:
                change = 0
                change_pct = 0

            results.append({
                'name': name,
                'symbol': symbol,
                'close': close,
                'high': high,
                'low': low,
                'open': open_price,
                'change': change,
                'change_pct': change_pct,
                'volume': volume
            })

            # Format output
            print("="*80)
            print("📊 " + name + " (" + symbol + ")")
            print("="*80)
            print("  Close:    $" + "{:.2f}".format(close))
            print("  High:     $" + "{:.2f}".format(high))
            print("  Low:      $" + "{:.2f}".format(low))
            print("  Open:     $" + "{:.2f}".format(open_price))

            if change > 0:
                change_symbol = "📈 UP"
            elif change < 0:
                change_symbol = "📉 DOWN"
            else:
                change_symbol = "➡️ FLAT"

            print("  Change:   " + change_symbol + " " + "{:.2f}".format(change) + " (" + "{:+.2f}".format(change_pct) + "%)")
            print("  Volume:   " + "{:,.0f}".format(volume))
            print()

    except Exception as e:
        print("="*80)
        print("❌ Error: " + str(e))
        print("="*80)
        print()

# Summary
print("="*80)
print("QUICK SUMMARY")
print("="*80)
print()

if results:
    for r in results:
        status = "📈 UP" if r['change'] > 0 else ("📉 DOWN" if r['change'] < 0 else "➡️ FLAT")
        pct_str = "{:.2f}".format(abs(r['change_pct']))
        price_str = "{:.2f}".format(r['close'])

        print(r['name'] + ": $" + price_str + " │ " + status + " " + pct_str + "%")

print()
print("="*80)
print("Last Updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print("Data Source: yfinance (Yahoo Finance - Real-time)")
print("="*80 + "\n")
