"""
Market Research - High Volatility Assets Analysis
Swing Trade Strategy (D1 Timeframe)

Focused on:
  - Stock Indices: NASDAQ, S&P 500, Dow Jones
  - Crypto: Bitcoin (BTC-USD)
  - Commodities: Gold, Oil
  - Forex: High volatility pairs

Run: python main_analysis.py
"""

import sys
sys.path.insert(0, 'src')

from data_loader import MarketDataLoader
from features import SwingTradeFeatures
from backtest import SwingTradeBacktest
import pandas as pd

def analyze_market(symbol, symbol_type='index', name="", days=365):
    """Analyze single market with swing trade strategy"""
    print(f"\n{'='*60}")
    print(f"ANALYZING: {name} ({symbol}) - D1 Daily")
    print(f"{'='*60}")

    # Load data
    loader = MarketDataLoader('data/raw')

    if symbol_type == 'index':
        df = loader.get_index_data(symbol, days=days)
    elif symbol_type == 'commodity':
        df = loader.get_commodity_data(symbol, days=days)
    elif symbol_type == 'forex':
        df = loader.get_forex_data(symbol, days=days)
    elif symbol_type == 'crypto':
        df = loader.get_crypto_data(symbol, days=days)

    if df is None or len(df) == 0:
        print(f"[FAIL] Failed to load {name}")
        return None

    print(f"[OK] Loaded {len(df)} candles")

    # Generate features
    print("Generating technical indicators...")
    try:
        df = SwingTradeFeatures.calculate_all_features(df)
        print(f"[OK] Generated features")
    except Exception as e:
        import traceback
        print(f"[ERROR] Error details:\n{traceback.format_exc()}")
        raise

    # Backtest
    print("Running backtest (initial capital: $10,000)...")
    backtest = SwingTradeBacktest(initial_capital=10000)
    trades = backtest.backtest(df)
    metrics = backtest.get_performance(trades)

    backtest.print_results(metrics)

    # Save results
    safe_name = name.replace('/', '-').replace(' ', '_')
    df.to_csv(f"data/processed/{safe_name}_analyzed.csv")
    trades.to_csv(f"results/{safe_name}_trades.csv")

    print(f"[OK] Saved analysis to data/processed/{safe_name}_analyzed.csv")
    print(f"[OK] Saved trades to results/{safe_name}_trades.csv")

    # Show last 5 signals
    signals = df[df['Signal'] != 0].tail(5)
    if len(signals) > 0:
        print(f"\nLast 5 Signals:")
        print(signals[['Close', 'RSI', 'MACD', 'Signal']])

    return df, trades, metrics


def main():
    """Analyze only HIGH VOLATILITY assets"""

    loader = MarketDataLoader()
    loader.print_available_assets()

    print("\n" + "="*60)
    print("STARTING HIGH VOLATILITY ANALYSIS")
    print("="*60)

    # === STOCK INDICES (NASDAQ, S&P 500, Dow Jones) ===
    print("\n" + "="*60)
    print("STOCK INDICES (High Volatility Only)")
    print("="*60)

    indices = [
        ("^IXIC", "NASDAQ-100"),
        ("^GSPC", "S&P 500"),
        ("^DJI", "Dow Jones"),
    ]

    index_results = {}
    for symbol, name in indices:
        try:
            result = analyze_market(symbol, symbol_type='index', name=name, days=365)
            if result:
                index_results[name] = result
        except Exception as e:
            print(f"[ERROR] Error: {e}")

    # === COMMODITIES (Gold, Oil) ===
    print("\n" + "="*60)
    print("COMMODITIES (High Volatility)")
    print("="*60)

    commodities = [
        ("GC=F", "Gold (Spot)"),
        ("CL=F", "Oil (WTI)"),
    ]

    commodity_results = {}
    for symbol, name in commodities:
        try:
            result = analyze_market(symbol, symbol_type='commodity', name=name, days=365)
            if result:
                commodity_results[name] = result
        except Exception as e:
            print(f"[ERROR] Error: {e}")

    # === FOREX (High Volatility Pairs) ===
    print("\n" + "="*60)
    print("FOREX (High Volatility Pairs)")
    print("="*60)

    forex_pairs = [
        ("GBPUSD=X", "GBP/USD"),
        ("EURUSD=X", "EUR/USD"),
        ("USDJPY=X", "USD/JPY"),
        ("AUDUSD=X", "AUD/USD"),
    ]

    forex_results = {}
    for symbol, name in forex_pairs:
        try:
            result = analyze_market(symbol, symbol_type='forex', name=name, days=365)
            if result:
                forex_results[name] = result
        except Exception as e:
            print(f"[ERROR] Error: {e}")

    # === CRYPTO (Bitcoin Only) ===
    print("\n" + "="*60)
    print("CRYPTOCURRENCY")
    print("="*60)

    try:
        crypto_result = analyze_market("BTC-USD", symbol_type='crypto', name="Bitcoin", days=365)
    except Exception as e:
        print(f"[ERROR] Error: {e}")

    # === SUMMARY ===
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE - HIGH VOLATILITY ASSETS")
    print("="*60)
    print("\nAnalyzed:")
    print(f"  {len(index_results)} Stock Indices")
    print(f"  {len(commodity_results)} Commodities")
    print(f"  {len(forex_results)} Forex Pairs")
    print(f"  1 Cryptocurrency (Bitcoin)")
    print(f"\nTotal Markets: {len(index_results) + len(commodity_results) + len(forex_results) + 1}")

    print("\nResults saved to:")
    print("  data/processed/   (analyzed data with indicators)")
    print("  results/          (trades & performance metrics)")

    print("\n" + "="*60)
    print("READY FOR TRADING!")
    print("="*60)


if __name__ == "__main__":
    main()
