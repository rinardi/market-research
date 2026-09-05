"""
Trend Analyzer - Detect price trend conditions (Uptrend, Downtrend, Consolidation)
"""
import pandas as pd
import numpy as np

class TrendAnalyzer:
    """Analyze price trends and market conditions"""

    @staticmethod
    def analyze_trend(df, period=20):
        """
        Detect trend condition
        Returns: 'UPTREND', 'DOWNTREND', 'CONSOLIDATION'
        """
        if len(df) < period:
            return 'UNKNOWN', {}

        # Convert Close to numeric
        if 'Close' in df.columns:
            close = pd.to_numeric(df['Close'], errors='coerce').iloc[-period:]
        else:
            return 'UNKNOWN', {}

        close = close.dropna()

        # Convert High to numeric
        if 'High' in df.columns:
            high = pd.to_numeric(df['High'], errors='coerce').iloc[-period:].dropna()
        else:
            high = close

        # Convert Low to numeric
        if 'Low' in df.columns:
            low = pd.to_numeric(df['Low'], errors='coerce').iloc[-period:].dropna()
        else:
            low = close

        # Calculate trend strength
        current_price = close.iloc[-1]
        period_high = high.max()
        period_low = low.min()
        period_range = period_high - period_low

        # Price position in range (0-100)
        if period_range > 0:
            price_position = ((current_price - period_low) / period_range) * 100
        else:
            price_position = 50

        # Higher High / Lower Low check (last 5 candles)
        if len(close) >= 5:
            recent_close = close.iloc[-5:]
            recent_high = high.iloc[-5:] if 'High' in df.columns else recent_close
            recent_low = low.iloc[-5:] if 'Low' in df.columns else recent_close

            higher_highs = sum(1 for i in range(1, len(recent_high)) if recent_high.iloc[i] > recent_high.iloc[i-1])
            lower_lows = sum(1 for i in range(1, len(recent_low)) if recent_low.iloc[i] < recent_low.iloc[i-1])

            if higher_highs >= 3:
                trend = 'UPTREND'
            elif lower_lows >= 3:
                trend = 'DOWNTREND'
            else:
                trend = 'CONSOLIDATION'
        else:
            trend = 'CONSOLIDATION'

        # Calculate momentum
        momentum = ((close.iloc[-1] - close.iloc[0]) / close.iloc[0]) * 100

        # Calculate volatility
        returns = close.pct_change()
        volatility = returns.std() * 100

        trend_data = {
            'trend': trend,
            'price_position': round(price_position, 1),
            'momentum': round(momentum, 2),
            'volatility': round(volatility, 2),
            'period_high': round(period_high, 2),
            'period_low': round(period_low, 2),
            'current_price': round(current_price, 2),
            'support': round(period_low, 2),
            'resistance': round(period_high, 2),
        }

        return trend, trend_data

    @staticmethod
    def get_trend_emoji(trend):
        """Get emoji for trend"""
        if trend == 'UPTREND':
            return '📈'
        elif trend == 'DOWNTREND':
            return '📉'
        else:
            return '➡️'

    @staticmethod
    def get_trend_description(trend):
        """Get description for trend"""
        descriptions = {
            'UPTREND': 'Price making Higher Highs & Higher Lows - Bullish',
            'DOWNTREND': 'Price making Lower Highs & Lower Lows - Bearish',
            'CONSOLIDATION': 'Price trading sideways - Range bound',
            'UNKNOWN': 'Not enough data'
        }
        return descriptions.get(trend, 'Unknown')

    @staticmethod
    def get_price_levels(df, period=20):
        """Get support and resistance levels"""
        if len(df) < period:
            return 0, 0

        try:
            if 'High' in df.columns:
                high = pd.to_numeric(df['High'].iloc[-period:], errors='coerce').dropna()
            else:
                high = pd.to_numeric(df['Close'].iloc[-period:], errors='coerce').dropna()

            if 'Low' in df.columns:
                low = pd.to_numeric(df['Low'].iloc[-period:], errors='coerce').dropna()
            else:
                low = pd.to_numeric(df['Close'].iloc[-period:], errors='coerce').dropna()

            if len(high) == 0 or len(low) == 0:
                return 0, 0

            resistance = high.max()
            support = low.min()

            return float(support), float(resistance)
        except:
            return 0, 0

    @staticmethod
    def get_price_strength(df, period=5):
        """Get how strong the current move is (0-100)"""
        if len(df) < period:
            return 50

        try:
            close = pd.to_numeric(df['Close'].iloc[-period:], errors='coerce').dropna()

            if 'High' in df.columns:
                high = pd.to_numeric(df['High'].iloc[-period:], errors='coerce').dropna()
            else:
                high = close

            if 'Low' in df.columns:
                low = pd.to_numeric(df['Low'].iloc[-period:], errors='coerce').dropna()
            else:
                low = close

            if len(close) == 0:
                return 50

            period_high = high.max()
            period_low = low.min()
            period_range = period_high - period_low

            if period_range > 0:
                strength = ((close.iloc[-1] - period_low) / period_range) * 100
            else:
                strength = 50

            return round(strength, 1)
        except:
            return 50

    @staticmethod
    def analyze_ma_cross(df):
        """Check if moving averages are in bullish/bearish arrangement"""
        if 'EMA_10' not in df.columns or 'EMA_20' not in df.columns or 'EMA_50' not in df.columns:
            return None

        try:
            ema10 = float(pd.to_numeric(df['EMA_10'].iloc[-1], errors='coerce'))
            ema20 = float(pd.to_numeric(df['EMA_20'].iloc[-1], errors='coerce'))
            ema50 = float(pd.to_numeric(df['EMA_50'].iloc[-1], errors='coerce'))

            if pd.isna([ema10, ema20, ema50]).any():
                return None

            # Bullish arrangement: EMA10 > EMA20 > EMA50
            if ema10 > ema20 > ema50:
                return 'BULLISH'
            # Bearish arrangement: EMA10 < EMA20 < EMA50
            elif ema10 < ema20 < ema50:
                return 'BEARISH'
            else:
                return 'MIXED'
        except:
            return None

    @staticmethod
    def generate_trend_report(df, market_name):
        """Generate complete trend report"""
        trend, trend_data = TrendAnalyzer.analyze_trend(df)
        ma_arrangement = TrendAnalyzer.analyze_ma_cross(df)
        price_strength = TrendAnalyzer.get_price_strength(df)

        support, resistance = TrendAnalyzer.get_price_levels(df)

        report = {
            'market': market_name,
            'trend': trend,
            'emoji': TrendAnalyzer.get_trend_emoji(trend),
            'description': TrendAnalyzer.get_trend_description(trend),
            'current_price': trend_data.get('current_price', 0),
            'support': support,
            'resistance': resistance,
            'price_position': trend_data.get('price_position', 50),
            'momentum': trend_data.get('momentum', 0),
            'volatility': trend_data.get('volatility', 0),
            'ma_arrangement': ma_arrangement,
            'price_strength': price_strength,
        }

        return report


# Example usage
if __name__ == "__main__":
    import os
    from glob import glob

    print("\n" + "="*70)
    print("MARKET TREND ANALYSIS")
    print("="*70)

    # Analyze all processed markets
    csv_files = glob("data/processed/*_analyzed.csv")

    for csv_file in sorted(csv_files):
        try:
            market_name = os.path.basename(csv_file).replace('_analyzed.csv', '')
            df = pd.read_csv(csv_file)

            # Handle index properly
            if 'Date' in df.columns:
                df.set_index('Date', inplace=True)
            elif 'Ticker' in df.columns:
                df.set_index('Ticker', inplace=True)

            report = TrendAnalyzer.generate_trend_report(df, market_name)

            print(f"\n{report['emoji']} {market_name.upper()}")
            print("-" * 70)
            print(f"Trend:           {report['trend']}")
            print(f"Description:     {report['description']}")
            print(f"Current Price:   ${report['current_price']:,.2f}")
            print(f"Support:         ${report['support']:,.2f}")
            print(f"Resistance:      ${report['resistance']:,.2f}")
            print(f"Price Level:     {report['price_position']:.1f}% (0=Support, 100=Resistance)")
            print(f"Momentum:        {report['momentum']:+.2f}%")
            print(f"Volatility:      {report['volatility']:.2f}%")
            print(f"MA Arrangement:  {report['ma_arrangement']}")
            print(f"Price Strength:  {report['price_strength']:.1f}/100")

        except Exception as e:
            print(f"[ERROR] {market_name}: {e}")

    print("\n" + "="*70)
