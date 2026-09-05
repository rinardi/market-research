"""
Update HTML Dashboard with latest analysis results
Reads from CSV results and sends Telegram notifications
"""

import sys
sys.path.insert(0, 'src')

import pandas as pd
import os
import json
from datetime import datetime
from notifier import create_notifier_from_env

# Market definitions
MARKETS = {
    'NASDAQ-100': {'type': 'index', 'category': 'indices'},
    'S&P 500': {'type': 'index', 'category': 'indices'},
    'Dow Jones': {'type': 'index', 'category': 'indices'},
    'Gold (Spot)': {'type': 'commodity', 'category': 'commodities'},
    'Oil (WTI)': {'type': 'commodity', 'category': 'commodities'},
    'GBP-USD': {'type': 'forex', 'category': 'forex'},
    'EUR-USD': {'type': 'forex', 'category': 'forex'},
    'USD-JPY': {'type': 'forex', 'category': 'forex'},
    'AUD-USD': {'type': 'forex', 'category': 'forex'},
    'Bitcoin': {'type': 'crypto', 'category': 'crypto'},
}

def read_market_analysis(market_name):
    """Read market analysis from CSV"""
    try:
        csv_file = f"data/processed/{market_name}_analyzed.csv"
        if not os.path.exists(csv_file):
            return None

        df = pd.read_csv(csv_file, index_col='Date', parse_dates=True)

        # Get latest data
        latest = df.iloc[-1]
        last_signal_row = df[df['Signal'] != 0].iloc[-1] if len(df[df['Signal'] != 0]) > 0 else None

        market_data = {
            'name': market_name,
            'price': float(latest['Close']) if isinstance(latest['Close'], (int, float)) else float(str(latest['Close']).split()[0]),
            'rsi': float(latest['RSI']) if pd.notna(latest['RSI']) else 0,
            'macd': float(latest['MACD']) if pd.notna(latest['MACD']) else 0,
            'ema_20': float(latest['EMA_20']) if pd.notna(latest['EMA_20']) else 0,
            'adx': float(latest['ADX']) if pd.notna(latest['ADX']) else 0,
            'signal': int(latest['Signal']) if pd.notna(latest['Signal']) else 0,
        }

        # Read trade results
        trades_file = f"results/{market_name}_trades.csv"
        if os.path.exists(trades_file):
            trades_df = pd.read_csv(trades_file)
            if len(trades_df) > 0:
                win_trades = len(trades_df[trades_df['Return%'] > 0]) if 'Return%' in trades_df.columns else 0
                total_trades = len(trades_df[trades_df['Type'] == 'SELL']) if 'Type' in trades_df.columns else len(trades_df)
                win_rate = (win_trades / total_trades * 100) if total_trades > 0 else 0
                total_return = (trades_df['Return%'].sum() if 'Return%' in trades_df.columns else 0)

                market_data['win_rate'] = win_rate
                market_data['total_trades'] = total_trades
                market_data['total_return'] = total_return
            else:
                market_data['win_rate'] = 0
                market_data['total_trades'] = 0
                market_data['total_return'] = 0
        else:
            market_data['win_rate'] = 0
            market_data['total_trades'] = 0
            market_data['total_return'] = 0

        return market_data

    except Exception as e:
        print(f"[ERROR] Reading {market_name}: {e}")
        return None

def generate_html_data(markets_dict):
    """Generate data for HTML dashboard"""
    html_data = {
        'indices': [],
        'commodities': [],
        'forex': [],
        'crypto': [],
        'summary': {}
    }

    all_markets = []

    for market_name, config in markets_dict.items():
        market_data = read_market_analysis(market_name)
        if market_data:
            # Map signal
            signal_map = {1: 'BUY', -1: 'SELL', 0: 'HOLD'}
            market_data['signal_text'] = signal_map.get(market_data['signal'], 'HOLD')
            market_data['symbol'] = market_name.replace(' ', '_').upper()
            market_data['category'] = config['category']

            category = config['category']
            html_data[category].append(market_data)
            all_markets.append(market_data)

    # Calculate summary
    if all_markets:
        total_return = sum([m.get('total_return', 0) for m in all_markets]) / len(all_markets)
        best_market = max(all_markets, key=lambda x: x.get('total_return', 0))
        avg_win_rate = sum([m.get('win_rate', 0) for m in all_markets]) / len(all_markets)

        html_data['summary'] = {
            'total_return': total_return,
            'best_market': best_market['name'],
            'avg_win_rate': avg_win_rate,
            'total_markets': len(all_markets),
            'active_signals': sum(1 for m in all_markets if m['signal_text'] != 'HOLD')
        }

    return html_data

def update_html_dashboard(html_data):
    """Update dashboard.html with new data"""
    try:
        # Read current HTML
        with open('dashboard.html', 'r') as f:
            html = f.read()

        # Create JavaScript data
        js_markets = {
            'indices': html_data.get('indices', []),
            'commodities': html_data.get('commodities', []),
            'forex': html_data.get('forex', []),
            'crypto': html_data.get('crypto', [])
        }

        # Replace market data in HTML
        json_data = json.dumps(js_markets)
        html = html.replace(
            "const marketData = {",
            f"const marketData = {json_data};\n\n        const legacyMarketData = {{"
        )

        # Update summary values
        summary = html_data.get('summary', {})
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write back updated HTML
        with open('dashboard.html', 'w') as f:
            f.write(html)

        print(f"[OK] Dashboard updated at {timestamp}")
        return True

    except Exception as e:
        print(f"[ERROR] Updating dashboard: {e}")
        return False

def send_notifications(html_data):
    """Send Telegram notifications"""
    notifier = create_notifier_from_env()
    if not notifier:
        print("[WARNING] Notifier not configured, skipping notifications")
        return

    # Format market data for notifier
    markets_for_notification = {
        'indices': html_data.get('indices', []),
        'commodities': html_data.get('commodities', []),
        'forex': html_data.get('forex', []),
        'crypto': html_data.get('crypto', [])
    }

    # Check for new signals
    new_buy_signals = [m for m in (markets_for_notification.get('indices', []) +
                                    markets_for_notification.get('commodities', []) +
                                    markets_for_notification.get('forex', []) +
                                    markets_for_notification.get('crypto', []))
                      if m.get('signal_text') == 'BUY']

    new_sell_signals = [m for m in (markets_for_notification.get('indices', []) +
                                     markets_for_notification.get('commodities', []) +
                                     markets_for_notification.get('forex', []) +
                                     markets_for_notification.get('crypto', []))
                       if m.get('signal_text') == 'SELL']

    # Send summary
    print("[OK] Sending market summary to Telegram...")
    notifier.send_market_summary(markets_for_notification)

    # Send individual signal alerts
    for market in new_buy_signals:
        print(f"[OK] Sending BUY signal for {market['name']}...")
        indicators = {
            'RSI': market.get('rsi', 0),
            'MACD': market.get('macd', 0),
            'EMA_20': market.get('ema_20', 0),
            'ADX': market.get('adx', 0)
        }
        notifier.send_trade_alert(market['name'], 'BUY', market.get('price', 0), indicators)

    for market in new_sell_signals:
        print(f"[OK] Sending SELL signal for {market['name']}...")
        indicators = {
            'RSI': market.get('rsi', 0),
            'MACD': market.get('macd', 0),
            'EMA_20': market.get('ema_20', 0),
            'ADX': market.get('adx', 0)
        }
        notifier.send_trade_alert(market['name'], 'SELL', market.get('price', 0), indicators)

def main():
    """Main update function"""
    print("\n" + "="*60)
    print("UPDATING DASHBOARD & SENDING NOTIFICATIONS")
    print("="*60)

    # Generate data from CSV files
    html_data = generate_html_data(MARKETS)

    # Update HTML dashboard
    update_html_dashboard(html_data)

    # Send notifications
    send_notifications(html_data)

    print("\n" + "="*60)
    print("UPDATE COMPLETE")
    print("Open dashboard.html in browser to view live data")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
