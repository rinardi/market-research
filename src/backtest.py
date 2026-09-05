"""
Backtesting Engine for Swing Trade Strategy
"""
import pandas as pd
import numpy as np

class SwingTradeBacktest:
    """Backtest swing trade strategy"""

    def __init__(self, initial_capital=10000, position_size=0.95):
        self.initial_capital = initial_capital
        self.position_size = position_size  # 95% of capital per trade
        self.capital = initial_capital
        self.position = 0  # Current position (shares held)
        self.entry_price = 0
        self.trades = []

    def backtest(self, df):
        """
        Run backtest on dataframe with Signal column
        Returns: trades dataframe with performance metrics
        """
        for idx, row in df.iterrows():
            signal = row['Signal'] if not isinstance(row['Signal'], pd.Series) else row['Signal'].item()
            price = row['Close'] if not isinstance(row['Close'], pd.Series) else row['Close'].item()

            # BUY Signal
            if signal == 1 and self.position == 0:
                shares = (self.capital * self.position_size) / price
                self.position = shares
                self.entry_price = price
                self.trades.append({
                    'Date': idx,
                    'Type': 'BUY',
                    'Price': price,
                    'Shares': shares,
                    'Capital': self.capital
                })

            # SELL Signal
            elif signal == -1 and self.position > 0:
                exit_price = price
                pnl = (exit_price - self.entry_price) * self.position
                self.capital += pnl

                self.trades.append({
                    'Date': idx,
                    'Type': 'SELL',
                    'Price': exit_price,
                    'Shares': self.position,
                    'PnL': pnl,
                    'Return%': (pnl / (self.entry_price * self.position)) * 100,
                    'Capital': self.capital
                })

                self.position = 0

        # Close any open position at last price
        if self.position > 0:
            last_row = df.iloc[-1]
            last_price = last_row['Close'] if not isinstance(last_row['Close'], pd.Series) else last_row['Close'].item()
            pnl = (last_price - self.entry_price) * self.position
            self.capital += pnl

        trades_df = pd.DataFrame(self.trades)
        return trades_df

    def get_performance(self, trades_df):
        """Calculate performance metrics"""
        if len(trades_df) == 0:
            return None

        total_return = ((self.capital - self.initial_capital) / self.initial_capital) * 100
        win_trades = len(trades_df[trades_df['Return%'] > 0]) if 'Return%' in trades_df.columns else 0
        total_trades = len(trades_df[trades_df['Type'] == 'SELL']) if 'Type' in trades_df.columns else 0
        win_rate = (win_trades / total_trades * 100) if total_trades > 0 else 0

        avg_win = trades_df[trades_df['Return%'] > 0]['Return%'].mean() if 'Return%' in trades_df.columns and len(trades_df[trades_df['Return%'] > 0]) > 0 else 0
        avg_loss = trades_df[trades_df['Return%'] < 0]['Return%'].mean() if 'Return%' in trades_df.columns and len(trades_df[trades_df['Return%'] < 0]) > 0 else 0

        metrics = {
            'Initial Capital': self.initial_capital,
            'Final Capital': self.capital,
            'Total Return %': total_return,
            'Win Rate %': win_rate,
            'Total Trades': total_trades,
            'Average Win %': avg_win,
            'Average Loss %': avg_loss,
            'Profit Factor': abs(avg_win / avg_loss) if avg_loss != 0 else 0
        }

        return metrics

    def print_results(self, metrics):
        """Print backtest results"""
        if metrics is None:
            print("[INFO] No trades to report")
            return

        print("\n" + "="*50)
        print("BACKTEST RESULTS")
        print("="*50)
        for key, value in metrics.items():
            try:
                if isinstance(value, (float, np.floating)):
                    print(f"{key:.<30} {value:>10.2f}")
                else:
                    print(f"{key:.<30} {value:>10}")
            except:
                print(f"{key:.<30} {str(value):>10}")
        print("="*50 + "\n")
