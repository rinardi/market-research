"""
Feature Engineering for Swing Trade
D1 timeframe indicators - Manual implementation
"""
import pandas as pd
import numpy as np

class SwingTradeFeatures:
    """Generate swing trade signals using technical indicators"""

    @staticmethod
    def add_moving_averages(df, short=10, medium=20, long=50):
        """Add EMA indicators"""
        close = df['Close'].squeeze() if isinstance(df['Close'], pd.DataFrame) else df['Close']
        df['EMA_10'] = close.ewm(span=short, adjust=False).mean().values
        df['EMA_20'] = close.ewm(span=medium, adjust=False).mean().values
        df['EMA_50'] = close.ewm(span=long, adjust=False).mean().values
        return df

    @staticmethod
    def add_rsi(df, period=14, overbought=70, oversold=30):
        """Add RSI for momentum"""
        close = df['Close'].squeeze() if isinstance(df['Close'], pd.DataFrame) else df['Close']
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = (100 - (100 / (1 + rs))).values
        df['RSI_Signal'] = 0
        df.loc[df['RSI'] > overbought, 'RSI_Signal'] = -1
        df.loc[df['RSI'] < oversold, 'RSI_Signal'] = 1
        return df

    @staticmethod
    def add_macd(df, fast=12, slow=26, signal=9):
        """Add MACD for trend confirmation"""
        close = df['Close'].squeeze() if isinstance(df['Close'], pd.DataFrame) else df['Close']
        ema_fast = close.ewm(span=fast, adjust=False).mean()
        ema_slow = close.ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        df['MACD'] = macd.values
        df['MACD_Signal'] = macd.ewm(span=signal, adjust=False).mean().values
        df['MACD_Diff'] = (macd - df['MACD_Signal']).values
        return df

    @staticmethod
    def add_bollinger_bands(df, period=20, std=2):
        """Add Bollinger Bands for volatility"""
        close = df['Close']
        if isinstance(close, pd.DataFrame):
            close = close.squeeze()

        middle = close.rolling(window=period).mean()
        volatility = close.rolling(window=period).std()

        df['BB_Middle'] = middle.values
        df['BB_Upper'] = (middle + volatility * std).values
        df['BB_Lower'] = (middle - volatility * std).values
        return df

    @staticmethod
    def add_atr(df, period=14):
        """Add ATR for volatility"""
        high = df['High'].squeeze() if isinstance(df['High'], pd.DataFrame) else df['High']
        low = df['Low'].squeeze() if isinstance(df['Low'], pd.DataFrame) else df['Low']
        close = df['Close'].squeeze() if isinstance(df['Close'], pd.DataFrame) else df['Close']

        high_low = high - low
        high_close = abs(high - close.shift())
        low_close = abs(low - close.shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['ATR'] = tr.rolling(window=period).mean().values
        return df

    @staticmethod
    def add_adx(df, period=14, trend_threshold=25):
        """Add ADX for trend strength (simplified)"""
        high = df['High'].squeeze() if isinstance(df['High'], pd.DataFrame) else df['High']
        low = df['Low'].squeeze() if isinstance(df['Low'], pd.DataFrame) else df['Low']

        high_diff = high.diff()
        low_diff = -low.diff()

        plus_dm = high_diff.where((high_diff > low_diff) & (high_diff > 0), 0)
        minus_dm = low_diff.where((low_diff > high_diff) & (low_diff > 0), 0)

        tr = (high - low).rolling(window=period).mean()
        plus_di = 100 * (plus_dm.rolling(window=period).mean() / tr)
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / tr)

        df['ADX'] = abs(plus_di - minus_di).rolling(window=period).mean().values
        df['Trend_Strength'] = df['ADX'] > trend_threshold
        return df

    @staticmethod
    def generate_swing_signals(df):
        """
        Generate buy/sell signals for swing trading
        Signal: 1 = BUY, -1 = SELL, 0 = HOLD
        """
        close = df['Close'].squeeze() if isinstance(df['Close'], pd.DataFrame) else df['Close']

        df['Signal'] = 0

        # BUY Signals: Price above EMA20, RSI oversold recovery, MACD positive
        buy_condition = (
            (close > df['EMA_20']) &
            (df['RSI'] < 50) &
            (df['MACD'] > df['MACD_Signal']) &
            (df['ADX'] > 20)
        )
        df.loc[buy_condition.values, 'Signal'] = 1

        # SELL Signals: Price below EMA20, RSI overbought, MACD negative
        sell_condition = (
            (close < df['EMA_20']) &
            (df['RSI'] > 50) &
            (df['MACD'] < df['MACD_Signal']) &
            (df['ADX'] > 20)
        )
        df.loc[sell_condition.values, 'Signal'] = -1

        return df

    @staticmethod
    def calculate_all_features(df):
        """Calculate all features and generate signals"""
        df = SwingTradeFeatures.add_moving_averages(df)
        df = SwingTradeFeatures.add_rsi(df)
        df = SwingTradeFeatures.add_macd(df)
        df = SwingTradeFeatures.add_bollinger_bands(df)
        df = SwingTradeFeatures.add_atr(df)
        df = SwingTradeFeatures.add_adx(df)
        df = SwingTradeFeatures.generate_swing_signals(df)

        return df.dropna()
