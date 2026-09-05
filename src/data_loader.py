"""
Market Data Loader - High Volatility Assets Only
Stock Indices, Crypto, Commodities, Forex
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

class MarketDataLoader:
    """Load D1 data from high-volatility assets only"""

    def __init__(self, data_dir="data/raw"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

        # High volatility assets
        self.indices = {
            "^GSPC": "S&P 500",
            "^IXIC": "NASDAQ",
            "^DJI": "Dow Jones",
            "^FTSE": "FTSE 100",
            "^N225": "Nikkei 225",
            "^HSIO": "Hang Seng"
        }

        self.commodities = {
            "GC=F": "Gold (Spot)",
            "CL=F": "Oil (WTI)",
            "NG=F": "Natural Gas",
            "SI=F": "Silver"
        }

        self.forex_pairs = {
            "EURUSD=X": "EUR/USD",
            "GBPUSD=X": "GBP/USD",
            "USDJPY=X": "USD/JPY",
            "AUDUSD=X": "AUD/USD",
            "NZDUSD=X": "NZD/USD",
            "USDCAD=X": "USD/CAD",
            "USDCHF=X": "USD/CHF",
            "GBPJPY=X": "GBP/JPY",
            "EURJPY=X": "EUR/JPY",
            "AUDJPY=X": "AUD/JPY"
        }

        self.crypto = {
            "BTC-USD": "Bitcoin"
        }

    def get_index_data(self, symbol, days=365, start_date=None, end_date=None):
        """
        Get stock index data

        Args:
            symbol: Stock index symbol (e.g., '^IXIC')
            days: Number of days to fetch (if start_date/end_date not provided)
            start_date: Custom start date (format: 'YYYY-MM-DD')
            end_date: Custom end date (format: 'YYYY-MM-DD')
        """
        name = self.indices.get(symbol, symbol)

        # Use custom dates or calculate from days
        if end_date is None:
            end_date = datetime.now()
        else:
            end_date = pd.to_datetime(end_date)

        if start_date is None:
            start_date = end_date - timedelta(days=days)
        else:
            start_date = pd.to_datetime(start_date)

        days_str = (end_date - start_date).days
        print(f"Fetching {name} (D1) - Last {days_str} days ({start_date.date()} to {end_date.date()})...")

        try:
            df = yf.download(symbol, start=start_date, end=end_date, interval='1d')

            if df is None or len(df) == 0:
                print(f"[ERROR] No data returned for {name}")
                return None

            df.index.name = 'Date'

            filepath = os.path.join(self.data_dir, f"{symbol.replace('^', '')}.csv")
            df.to_csv(filepath)
            print(f"[OK] {name} saved ({len(df)} rows)")

            return df
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            return None

    def get_commodity_data(self, symbol, days=365, start_date=None, end_date=None):
        """
        Get commodity futures data (Gold, Oil)

        Args:
            symbol: Commodity symbol (e.g., 'GC=F', 'CL=F')
            days: Number of days to fetch (if start_date/end_date not provided)
            start_date: Custom start date (format: 'YYYY-MM-DD')
            end_date: Custom end date (format: 'YYYY-MM-DD')
        """
        name = self.commodities.get(symbol, symbol)

        # Use custom dates or calculate from days
        if end_date is None:
            end_date = datetime.now()
        else:
            end_date = pd.to_datetime(end_date)

        if start_date is None:
            start_date = end_date - timedelta(days=days)
        else:
            start_date = pd.to_datetime(start_date)

        days_str = (end_date - start_date).days
        print(f"Fetching {name} (D1) - Last {days_str} days ({start_date.date()} to {end_date.date()})...")

        try:
            df = yf.download(symbol, start=start_date, end=end_date, interval='1d')

            if df is None or len(df) == 0:
                print(f"[ERROR] No data returned for {name}")
                return None

            df.index.name = 'Date'

            filepath = os.path.join(self.data_dir, f"{symbol.replace('=F', '')}.csv")
            df.to_csv(filepath)
            print(f"[OK] {name} saved ({len(df)} rows)")

            return df
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            return None

    def get_forex_data(self, symbol, days=365, start_date=None, end_date=None):
        """
        Get high volatility forex pairs

        Args:
            symbol: Forex pair symbol (e.g., 'EURUSD=X')
            days: Number of days to fetch (if start_date/end_date not provided)
            start_date: Custom start date (format: 'YYYY-MM-DD')
            end_date: Custom end date (format: 'YYYY-MM-DD')
        """
        name = self.forex_pairs.get(symbol, symbol)

        # Use custom dates or calculate from days
        if end_date is None:
            end_date = datetime.now()
        else:
            end_date = pd.to_datetime(end_date)

        if start_date is None:
            start_date = end_date - timedelta(days=days)
        else:
            start_date = pd.to_datetime(start_date)

        days_str = (end_date - start_date).days
        print(f"Fetching {name} (D1) - Last {days_str} days ({start_date.date()} to {end_date.date()})...")

        try:
            df = yf.download(symbol, start=start_date, end=end_date, interval='1d')

            if df is None or len(df) == 0:
                print(f"[ERROR] No data returned for {name}")
                return None

            df.index.name = 'Date'

            filepath = os.path.join(self.data_dir, f"{symbol.replace('=X', '')}.csv")
            df.to_csv(filepath)
            print(f"[OK] {name} saved ({len(df)} rows)")

            return df
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            return None

    def get_crypto_data(self, symbol="BTC-USD", days=365, start_date=None, end_date=None):
        """
        Get Bitcoin data only

        Args:
            symbol: Crypto symbol (default: 'BTC-USD')
            days: Number of days to fetch (if start_date/end_date not provided)
            start_date: Custom start date (format: 'YYYY-MM-DD')
            end_date: Custom end date (format: 'YYYY-MM-DD')
        """
        # Use custom dates or calculate from days
        if end_date is None:
            end_date = datetime.now()
        else:
            end_date = pd.to_datetime(end_date)

        if start_date is None:
            start_date = end_date - timedelta(days=days)
        else:
            start_date = pd.to_datetime(start_date)

        days_str = (end_date - start_date).days
        print(f"Fetching Bitcoin (D1) - Last {days_str} days ({start_date.date()} to {end_date.date()})...")

        try:
            df = yf.download(symbol, start=start_date, end=end_date, interval='1d')

            if df is None or len(df) == 0:
                print(f"[ERROR] No data returned for Bitcoin")
                return None

            df.index.name = 'Date'

            filepath = os.path.join(self.data_dir, "BTC_USD.csv")
            df.to_csv(filepath)
            print(f"[OK] Bitcoin saved ({len(df)} rows)")

            return df
        except Exception as e:
            print(f"[ERROR] Bitcoin: {e}")
            return None

    def load_local_data(self, filepath):
        """Load data from local CSV"""
        return pd.read_csv(filepath, index_col='Date', parse_dates=True)

    def print_available_assets(self):
        """Print all available high-volatility assets"""
        print("\n" + "="*60)
        print("HIGH VOLATILITY ASSETS AVAILABLE")
        print("="*60)

        print("\nSTOCK INDICES:")
        for sym, name in self.indices.items():
            print(f"  {sym:10} = {name}")

        print("\nCOMMODITIES:")
        for sym, name in self.commodities.items():
            print(f"  {sym:10} = {name}")

        print("\nFOREX (High Volatility):")
        for sym, name in self.forex_pairs.items():
            print(f"  {sym:10} = {name}")

        print("\nCRYPTO:")
        for sym, name in self.crypto.items():
            print(f"  {sym:10} = {name}")

        print("="*60 + "\n")
