"""
Sync Dashboard - Read CSV data and update HTML dashboard with real data
Run this after main_analysis.py to populate dashboard
"""

import sys
sys.path.insert(0, 'src')

import pandas as pd
import json
import os
from datetime import datetime
from trend_analyzer import TrendAnalyzer
from notifier import create_notifier_from_env

# Market definitions
MARKETS = {
    'NASDAQ-100': {'type': 'index', 'category': 'indices', 'symbol': '^IXIC'},
    'S&P 500': {'type': 'index', 'category': 'indices', 'symbol': '^GSPC'},
    'Dow Jones': {'type': 'index', 'category': 'indices', 'symbol': '^DJI'},
    'Gold (Spot)': {'type': 'commodity', 'category': 'commodities', 'symbol': 'GC=F'},
    'Oil (WTI)': {'type': 'commodity', 'category': 'commodities', 'symbol': 'CL=F'},
    'GBP-USD': {'type': 'forex', 'category': 'forex', 'symbol': 'GBPUSD=X'},
    'EUR-USD': {'type': 'forex', 'category': 'forex', 'symbol': 'EURUSD=X'},
    'USD-JPY': {'type': 'forex', 'category': 'forex', 'symbol': 'USDJPY=X'},
    'AUD-USD': {'type': 'forex', 'category': 'forex', 'symbol': 'AUDUSD=X'},
    'Bitcoin': {'type': 'crypto', 'category': 'crypto', 'symbol': 'BTC-USD'},
}

def read_market_data(market_name):
    """Read market data from CSV files"""
    try:
        # Read analyzed data
        csv_file = f"data/processed/{market_name}_analyzed.csv"
        if not os.path.exists(csv_file):
            return None

        df = pd.read_csv(csv_file)

        # Get latest row
        latest = df.iloc[-1]

        # Convert values to proper types
        market_data = {
            'name': market_name,
            'price': float(latest['Close']) if pd.notna(latest['Close']) else 0,
            'returnPct': 0,
            'winRate': 0,
            'trades': 0,
            'signal': 'HOLD',
            'rsi': float(latest['RSI']) if pd.notna(latest['RSI']) else 0,
            'macd': float(latest['MACD']) if pd.notna(latest['MACD']) else 0,
            'ema_20': float(latest['EMA_20']) if pd.notna(latest['EMA_20']) else 0,
            'adx': float(latest['ADX']) if pd.notna(latest['ADX']) else 0,
        }

        # Map signal
        signal_value = latest['Signal'] if pd.notna(latest['Signal']) else 0
        signal_map = {1: 'BUY', -1: 'SELL', 0: 'HOLD'}
        market_data['signal'] = signal_map.get(int(signal_value), 'HOLD')

        # Read trade results
        trades_file = f"results/{market_name}_trades.csv"
        if os.path.exists(trades_file):
            trades_df = pd.read_csv(trades_file)
            if len(trades_df) > 0:
                # Calculate returns
                if 'Return%' in trades_df.columns:
                    total_return = trades_df['Return%'].sum()
                    market_data['returnPct'] = total_return

                    win_trades = len(trades_df[trades_df['Return%'] > 0])
                    total_trades = len(trades_df[trades_df['Type'] == 'SELL'])
                    market_data['winRate'] = (win_trades / total_trades * 100) if total_trades > 0 else 0
                    market_data['trades'] = total_trades

        # Add trend analysis
        trend, trend_data = TrendAnalyzer.analyze_trend(df)
        market_data['trend'] = trend
        market_data['trendEmoji'] = TrendAnalyzer.get_trend_emoji(trend)
        market_data['momentum'] = trend_data.get('momentum', 0)
        market_data['volatility'] = trend_data.get('volatility', 0)
        market_data['priceStrength'] = TrendAnalyzer.get_price_strength(df)
        market_data['support'], market_data['resistance'] = TrendAnalyzer.get_price_levels(df)

        return market_data

    except Exception as e:
        print(f"[ERROR] Reading {market_name}: {e}")
        return None

def generate_dashboard_json():
    """Generate complete dashboard data"""
    dashboard_data = {
        'indices': [],
        'commodities': [],
        'forex': [],
        'crypto': [],
        'timestamp': datetime.now().isoformat(),
    }

    all_markets = []

    for market_name, config in MARKETS.items():
        market_data = read_market_data(market_name)
        if market_data:
            category = config['category']
            dashboard_data[category].append(market_data)
            all_markets.append(market_data)

    # Calculate summary
    if all_markets:
        total_return = sum([m.get('returnPct', 0) for m in all_markets]) / len(all_markets) if len(all_markets) > 0 else 0
        best_market = max(all_markets, key=lambda x: x.get('returnPct', 0)) if all_markets else None
        avg_win_rate = sum([m.get('winRate', 0) for m in all_markets]) / len(all_markets) if len(all_markets) > 0 else 0

        dashboard_data['summary'] = {
            'totalReturn': total_return,
            'bestMarket': best_market['name'] if best_market else 'N/A',
            'avgWinRate': avg_win_rate,
            'totalMarkets': len(all_markets),
            'activeSignals': sum(1 for m in all_markets if m['signal'] != 'HOLD'),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    return dashboard_data

def update_html_with_data():
    """Update HTML file with real data"""
    try:
        dashboard_data = generate_dashboard_json()

        # Read current HTML
        with open('dashboard.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Find and replace the marketData object
        import re

        # Create proper JSON string for JavaScript
        markets_json = json.dumps(dashboard_data)

        # Replace const marketData section
        pattern = r'const marketData = \{[\s\S]*?\};'
        replacement = f'const marketData = {markets_json};'

        new_html = re.sub(pattern, replacement, html_content)

        # Also update summary values in HTML
        summary = dashboard_data.get('summary', {})
        new_html = new_html.replace(
            'id="total-return">+12.5%',
            f'id="total-return">{summary.get("totalReturn", 0):+.2f}%'
        )
        new_html = new_html.replace(
            'id="best-performer" style="color: #667eea;">Oil WTI',
            f'id="best-performer" style="color: #667eea;">{summary.get("bestMarket", "N/A")}'
        )
        new_html = new_html.replace(
            'id="avg-win-rate" style="color: #667eea;">65%',
            f'id="avg-win-rate" style="color: #667eea;">{summary.get("avgWinRate", 0):.0f}%'
        )

        # Update last update time
        timestamp = datetime.now().strftime("%b %d, %Y %H:%M:%S")
        new_html = new_html.replace(
            'id="last-update">Loading...',
            f'id="last-update">{timestamp}'
        )

        # Write updated HTML
        with open('dashboard.html', 'w', encoding='utf-8') as f:
            f.write(new_html)

        print("[OK] Dashboard updated with real data")
        return True

    except Exception as e:
        print(f"[ERROR] Updating HTML: {e}")
        return False

def main():
    """Main sync function"""
    print("\n" + "="*60)
    print("SYNCING DASHBOARD WITH REAL DATA")
    print("="*60)

    # Update dashboard
    if update_html_with_data():
        print("[OK] Dashboard sync complete")
        print(f"[OK] Updated: {datetime.now()}")
        print("[OK] Open dashboard.html to view live data")
    else:
        print("[ERROR] Dashboard sync failed")

    print("="*60 + "\n")

if __name__ == "__main__":
    main()
