"""
Fetch Extended Historical Data (5-10 years)

This script allows fetching long-term historical data for better backtesting
and pattern recognition across multiple market cycles.

Run this ONCE to get extended data, or after initial setup.
"""

import sys
sys.path.insert(0, 'src')

from data_loader import MarketDataLoader
from data_validator import DataValidator
from datetime import datetime, timedelta
import pandas as pd

def fetch_extended_data(years=5):
    """Fetch extended historical data for all assets"""

    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)

    print(f"\n{'='*80}")
    print(f"FETCHING EXTENDED HISTORICAL DATA ({years} YEARS)")
    print(f"Period: {start_date.date()} to {end_date.date()}")
    print(f"{'='*80}")

    loader = MarketDataLoader('data/raw')

    results = {
        'success': [],
        'failed': [],
        'stats': {}
    }

    # === STOCK INDICES ===
    print(f"\n[1] STOCK INDICES")
    print("-" * 80)

    indices = [
        ("^IXIC", "NASDAQ-100"),
        ("^GSPC", "S&P 500"),
        ("^DJI", "Dow Jones"),
    ]

    for symbol, name in indices:
        print(f"\n  Fetching {name} ({symbol})...")
        try:
            df = loader.get_index_data(symbol, start_date=start_date, end_date=end_date)
            if df is not None and len(df) > 0:
                results['success'].append(name)
                results['stats'][name] = {
                    'rows': len(df),
                    'start': str(df.index[0].date()),
                    'end': str(df.index[-1].date())
                }
                print(f"    ✅ {len(df)} rows | {df.index[0].date()} to {df.index[-1].date()}")
            else:
                results['failed'].append(name)
                print(f"    ❌ Failed to fetch data")
        except Exception as e:
            results['failed'].append(name)
            print(f"    ❌ Error: {str(e)[:100]}")

    # === COMMODITIES ===
    print(f"\n[2] COMMODITIES")
    print("-" * 80)

    commodities = [
        ("GC=F", "Gold (Spot)"),
        ("CL=F", "Oil (WTI)"),
    ]

    for symbol, name in commodities:
        print(f"\n  Fetching {name} ({symbol})...")
        try:
            df = loader.get_commodity_data(symbol, start_date=start_date, end_date=end_date)
            if df is not None and len(df) > 0:
                results['success'].append(name)
                results['stats'][name] = {
                    'rows': len(df),
                    'start': str(df.index[0].date()),
                    'end': str(df.index[-1].date())
                }
                print(f"    ✅ {len(df)} rows | {df.index[0].date()} to {df.index[-1].date()}")
            else:
                results['failed'].append(name)
                print(f"    ❌ Failed to fetch data")
        except Exception as e:
            results['failed'].append(name)
            print(f"    ❌ Error: {str(e)[:100]}")

    # === FOREX ===
    print(f"\n[3] FOREX PAIRS (High Volatility)")
    print("-" * 80)

    forex_pairs = [
        ("EURUSD=X", "EUR/USD"),
        ("GBPUSD=X", "GBP/USD"),
        ("USDJPY=X", "USD/JPY"),
        ("AUDUSD=X", "AUD/USD"),
    ]

    for symbol, name in forex_pairs:
        print(f"\n  Fetching {name} ({symbol})...")
        try:
            df = loader.get_forex_data(symbol, start_date=start_date, end_date=end_date)
            if df is not None and len(df) > 0:
                results['success'].append(name)
                results['stats'][name] = {
                    'rows': len(df),
                    'start': str(df.index[0].date()),
                    'end': str(df.index[-1].date())
                }
                print(f"    ✅ {len(df)} rows | {df.index[0].date()} to {df.index[-1].date()}")
            else:
                results['failed'].append(name)
                print(f"    ❌ Failed to fetch data")
        except Exception as e:
            results['failed'].append(name)
            print(f"    ❌ Error: {str(e)[:100]}")

    # === CRYPTO ===
    print(f"\n[4] CRYPTOCURRENCY")
    print("-" * 80)

    print(f"\n  Fetching Bitcoin (BTC-USD)...")
    try:
        df = loader.get_crypto_data('BTC-USD', start_date=start_date, end_date=end_date)
        if df is not None and len(df) > 0:
            results['success'].append('Bitcoin')
            results['stats']['Bitcoin'] = {
                'rows': len(df),
                'start': str(df.index[0].date()),
                'end': str(df.index[-1].date())
            }
            print(f"    ✅ {len(df)} rows | {df.index[0].date()} to {df.index[-1].date()}")
        else:
            results['failed'].append('Bitcoin')
            print(f"    ❌ Failed to fetch data")
    except Exception as e:
        results['failed'].append('Bitcoin')
        print(f"    ❌ Error: {str(e)[:100]}")

    # === SUMMARY ===
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"\n✅ Successfully fetched: {len(results['success'])} assets")
    for asset in results['success']:
        if asset in results['stats']:
            stat = results['stats'][asset]
            print(f"   • {asset:20} | {stat['rows']:5} rows | {stat['start']} to {stat['end']}")

    if results['failed']:
        print(f"\n❌ Failed to fetch: {len(results['failed'])} assets")
        for asset in results['failed']:
            print(f"   • {asset}")

    print(f"\n{'='*80}")
    print(f"✅ Extended data fetch completed!")
    print(f"{'='*80}\n")

    return results


def validate_extended_data():
    """Validate all fetched data"""
    print(f"\n{'='*80}")
    print(f"VALIDATING EXTENDED DATA")
    print(f"{'='*80}")

    import os
    from pathlib import Path

    raw_dir = Path('data/raw')
    csv_files = list(raw_dir.glob('*.csv'))

    print(f"\nFound {len(csv_files)} CSV files in data/raw/\n")

    for csv_file in sorted(csv_files):
        print(f"Validating {csv_file.name}...")
        try:
            df = pd.read_csv(csv_file, index_col=0, parse_dates=True)

            # Get asset name
            asset_name = csv_file.stem.replace('_', '/').replace('USD', '').strip()

            # Run validation
            result = DataValidator.full_validation(df, asset_name=asset_name, verbose=False)

            # Print summary
            if result['result'] == 'PASS':
                print(f"  ✅ PASS | {result['rows']} rows")
            else:
                print(f"  ⚠️  ISSUES | {result['rows']} rows")
                for issue in result['issues'][:3]:  # Show first 3 issues
                    print(f"     {issue}")

        except Exception as e:
            print(f"  ❌ Error: {str(e)[:100]}")

    print(f"\n{'='*80}\n")


def main():
    """Main entry point"""

    print("\n" + "="*80)
    print("EXTENDED HISTORICAL DATA FETCHER")
    print("="*80)

    # Ask user for duration
    print("\nHow many years of historical data do you want?")
    print("  1. 2 years (recent trends)")
    print("  2. 5 years (recommended) - better pattern recognition")
    print("  3. 10 years (maximum) - multiple market cycles")

    choice = input("\nEnter choice (1-3, or press Enter for 5): ").strip()

    years_map = {
        '1': 2,
        '2': 5,
        '3': 10,
        '': 5  # Default
    }

    years = years_map.get(choice, 5)

    # Fetch data
    results = fetch_extended_data(years=years)

    # Validate data
    validate_extended_data()

    print("\n" + "="*80)
    print("✅ READY FOR ANALYSIS")
    print("="*80)
    print("\nNext steps:")
    print("  1. Run extended backtesting:")
    print("     python main_analysis.py")
    print("\n  2. Or analyze specific asset:")
    print("     python -c \"from src.data_loader import MarketDataLoader; ")
    print("               loader = MarketDataLoader(); ")
    print("               df = loader.get_index_data('^IXIC')\"")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
