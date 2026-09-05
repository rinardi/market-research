"""
Data Validator - Ensure raw data integrity and long-term reliability
Validates OHLCV data and detects issues
"""
import pandas as pd
import numpy as np
from datetime import datetime

class DataValidator:
    """Validate market data quality and integrity"""

    @staticmethod
    def validate_ohlc_relationships(df):
        """
        Check that High >= Close >= Open >= Low
        Returns list of issues found
        """
        issues = []

        # High should be >= all other prices
        if (df['High'] < df['Close']).any():
            count = (df['High'] < df['Close']).sum()
            issues.append(f"⚠️  {count} rows: High < Close")

        if (df['High'] < df['Open']).any():
            count = (df['High'] < df['Open']).sum()
            issues.append(f"⚠️  {count} rows: High < Open")

        if (df['High'] < df['Low']).any():
            count = (df['High'] < df['Low']).sum()
            issues.append(f"⚠️  {count} rows: High < Low")

        # Low should be <= all other prices
        if (df['Low'] > df['Close']).any():
            count = (df['Low'] > df['Close']).sum()
            issues.append(f"⚠️  {count} rows: Low > Close")

        if (df['Low'] > df['Open']).any():
            count = (df['Low'] > df['Open']).sum()
            issues.append(f"⚠️  {count} rows: Low > Open")

        return issues

    @staticmethod
    def validate_missing_values(df):
        """Check for NaN or null values"""
        issues = []
        missing = df.isnull().sum()

        if missing.any():
            for col, count in missing[missing > 0].items():
                issues.append(f"⚠️  {count} missing values in {col}")

        return issues

    @staticmethod
    def validate_volume(df):
        """Check volume data validity"""
        issues = []

        # Check for zero volume
        zero_volume = (df['Volume'] == 0).sum()
        if zero_volume > 0:
            issues.append(f"⚠️  {zero_volume} rows with zero volume")

        # Check for negative volume
        negative_volume = (df['Volume'] < 0).sum()
        if negative_volume > 0:
            issues.append(f"⚠️  {negative_volume} rows with negative volume")

        # Check for extreme volume outliers (>10x median)
        median_volume = df['Volume'].median()
        extreme = (df['Volume'] > median_volume * 10).sum()
        if extreme > 0:
            issues.append(f"ℹ️  {extreme} rows with extreme volume (>10x median)")

        return issues

    @staticmethod
    def validate_price_range(df):
        """Check for unrealistic price movements"""
        issues = []

        # Calculate daily returns
        df_copy = df.copy()
        df_copy['Return'] = (df_copy['Close'] - df_copy['Open']) / df_copy['Open']

        # Flag extreme daily moves (>25% in one day)
        extreme_moves = (abs(df_copy['Return']) > 0.25).sum()
        if extreme_moves > 0:
            issues.append(f"ℹ️  {extreme_moves} rows with >25% daily move (check for splits/errors)")

        # Flag moderate moves (>10%)
        large_moves = (abs(df_copy['Return']) > 0.10).sum()

        return issues, large_moves

    @staticmethod
    def validate_date_continuity(df):
        """Check for gaps in trading days"""
        issues = []

        if df.index.name != 'Date' and 'Date' not in df.columns:
            issues.append("⚠️  No Date index found")
            return issues

        # Get date index
        dates = pd.to_datetime(df.index) if isinstance(df.index, pd.DatetimeIndex) else pd.to_datetime(df['Date'])

        # Sort dates
        dates = sorted(dates)

        # Check for gaps > 2 days (accounts for weekends)
        gaps = []
        for i in range(1, len(dates)):
            gap = (dates[i] - dates[i-1]).days
            if gap > 2:
                gaps.append((dates[i-1], dates[i], gap))

        if gaps:
            issues.append(f"⚠️  {len(gaps)} date gaps found (>{2} days)")
            for start, end, days in gaps[:3]:  # Show first 3
                issues.append(f"    {start.date()} → {end.date()} ({days} days)")

        return issues

    @staticmethod
    def validate_data_freshness(df, max_age_days=7):
        """Check if data is recent (for live trading)"""
        issues = []

        # Get latest date
        if df.index.name == 'Date':
            latest_date = df.index[-1]
        elif 'Date' in df.columns:
            latest_date = pd.to_datetime(df['Date']).max()
        else:
            return ["⚠️  Cannot determine data age (no Date column)"]

        latest_date = pd.to_datetime(latest_date)
        age = (datetime.now() - latest_date).days

        if age > max_age_days:
            issues.append(f"⚠️  Data is {age} days old (stale)")
        elif age > 3:
            issues.append(f"ℹ️  Data is {age} days old (consider updating)")

        return issues

    @staticmethod
    def validate_column_structure(df):
        """Check for required columns"""
        issues = []
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']

        for col in required_cols:
            if col not in df.columns:
                issues.append(f"❌ Missing required column: {col}")

        return issues

    @staticmethod
    def full_validation(df, asset_name="", verbose=True):
        """Run all validations and return comprehensive report"""

        print(f"\n{'='*70}")
        print(f"DATA VALIDATION REPORT: {asset_name}")
        print(f"{'='*70}")

        all_issues = []

        # 1. Column structure
        print("\n[1] Column Structure...")
        issues = DataValidator.validate_column_structure(df)
        if issues:
            for issue in issues:
                print(f"    {issue}")
                all_issues.append(issue)
        else:
            print("    ✅ All required columns present")

        # 2. OHLC relationships
        print("\n[2] OHLC Relationships...")
        issues = DataValidator.validate_ohlc_relationships(df)
        if issues:
            for issue in issues:
                print(f"    {issue}")
                all_issues.append(issue)
        else:
            print("    ✅ All OHLC relationships valid")

        # 3. Missing values
        print("\n[3] Missing Values...")
        issues = DataValidator.validate_missing_values(df)
        if issues:
            for issue in issues:
                print(f"    {issue}")
                all_issues.append(issue)
        else:
            print("    ✅ No missing values found")

        # 4. Volume validation
        print("\n[4] Volume Validation...")
        issues = DataValidator.validate_volume(df)
        if issues:
            for issue in issues:
                print(f"    {issue}")
                all_issues.append(issue)
        else:
            print("    ✅ Volume data looks good")

        # 5. Price range
        print("\n[5] Price Movement Analysis...")
        issues, large_moves = DataValidator.validate_price_range(df)
        if issues:
            for issue in issues:
                print(f"    {issue}")
                all_issues.append(issue)
        print(f"    ℹ️  {large_moves} rows with >10% daily moves (normal for volatility assets)")

        # 6. Date continuity
        print("\n[6] Date Continuity...")
        issues = DataValidator.validate_date_continuity(df)
        if issues:
            for issue in issues:
                print(f"    {issue}")
                all_issues.append(issue)
        else:
            print("    ✅ Date continuity verified")

        # 7. Data freshness
        print("\n[7] Data Freshness...")
        issues = DataValidator.validate_data_freshness(df)
        if issues:
            for issue in issues:
                print(f"    {issue}")
                all_issues.append(issue)
        else:
            print("    ✅ Data is current")

        # Summary statistics
        print("\n[8] Data Summary...")
        print(f"    Rows:      {len(df):,}")
        print(f"    Columns:   {len(df.columns)}")
        print(f"    Date Range: {df.index[0] if hasattr(df.index, '__getitem__') else 'N/A'} to {df.index[-1] if hasattr(df.index, '__getitem__') else 'N/A'}")
        print(f"    Avg Volume: {df['Volume'].mean():,.0f}")
        print(f"    Price Range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")

        # Overall result
        print(f"\n{'='*70}")
        if not all_issues:
            print("✅ VALIDATION PASSED - Data quality is EXCELLENT")
            result = "PASS"
        else:
            print(f"⚠️  VALIDATION FOUND {len(all_issues)} ISSUE(S)")
            result = "ISSUES"
        print(f"{'='*70}\n")

        return {
            'result': result,
            'issues': all_issues,
            'rows': len(df),
            'date_range': (str(df.index[0]), str(df.index[-1])) if len(df) > 0 else None
        }


# Example usage
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from src.data_loader import MarketDataLoader

    # Validate sample data
    loader = MarketDataLoader('data/raw')

    # Check NASDAQ
    df = loader.get_index_data('^IXIC', days=365)
    if df is not None:
        DataValidator.full_validation(df, "NASDAQ-100 (^IXIC)")

    # Check Bitcoin
    df = loader.get_crypto_data('BTC-USD', days=365)
    if df is not None:
        DataValidator.full_validation(df, "Bitcoin (BTC-USD)")
