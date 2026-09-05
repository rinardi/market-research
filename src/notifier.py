"""
Notifier - Send alerts to Telegram/WhatsApp
"""
import requests
import json
from datetime import datetime

class TelegramNotifier:
    """Send messages to Telegram"""

    def __init__(self, bot_token, chat_id):
        """
        Initialize Telegram bot
        bot_token: Get from @BotFather on Telegram
        chat_id: Your Telegram user ID or group ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, text):
        """Send text message"""
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"[ERROR] Telegram send failed: {e}")
            return False

    def send_market_summary(self, markets_data):
        """Send market summary to Telegram"""
        message = self._format_market_summary(markets_data)
        return self.send_message(message)

    def send_trade_alert(self, market_name, signal_type, price, indicators):
        """Send trade alert"""
        message = self._format_trade_alert(market_name, signal_type, price, indicators)
        return self.send_message(message)

    def _format_market_summary(self, markets_data):
        """Format market summary message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Find best and worst performers
        all_markets = (
            markets_data.get('indices', []) +
            markets_data.get('commodities', []) +
            markets_data.get('forex', []) +
            markets_data.get('crypto', [])
        )

        if not all_markets:
            return "No market data available"

        best = max(all_markets, key=lambda x: x.get('return_pct', 0))
        worst = min(all_markets, key=lambda x: x.get('return_pct', 0))

        message = f"""
<b>SWING TRADING MONITOR</b>
<code>{timestamp}</code>

<b>TODAY HIGHLIGHTS:</b>
Top: <b>{best['name']}</b> +{best['return_pct']:.2f}%
Bottom: <b>{worst['name']}</b> {worst['return_pct']:.2f}%

<b>INDICES:</b>
"""

        for market in markets_data.get('indices', []):
            symbol = market['symbol']
            ret = market.get('return_pct', 0)
            signal = market.get('signal', 'HOLD')
            arrow = '📈' if ret > 0 else '📉' if ret < 0 else '➡️'
            message += f"{arrow} {symbol}: {ret:+.2f}% [{signal}]\n"

        message += "\n<b>COMMODITIES:</b>\n"
        for market in markets_data.get('commodities', []):
            symbol = market['symbol']
            ret = market.get('return_pct', 0)
            signal = market.get('signal', 'HOLD')
            arrow = '📈' if ret > 0 else '📉' if ret < 0 else '➡️'
            message += f"{arrow} {symbol}: {ret:+.2f}% [{signal}]\n"

        message += "\n<b>FOREX:</b>\n"
        for market in markets_data.get('forex', []):
            symbol = market['symbol']
            ret = market.get('return_pct', 0)
            signal = market.get('signal', 'HOLD')
            arrow = '📈' if ret > 0 else '📉' if ret < 0 else '➡️'
            message += f"{arrow} {symbol}: {ret:+.2f}% [{signal}]\n"

        message += "\n<b>CRYPTO:</b>\n"
        for market in markets_data.get('crypto', []):
            symbol = market['symbol']
            ret = market.get('return_pct', 0)
            signal = market.get('signal', 'HOLD')
            arrow = '📈' if ret > 0 else '📉' if ret < 0 else '➡️'
            message += f"{arrow} {symbol}: {ret:+.2f}% [{signal}]\n"

        message += "\n<i>Dashboard: Open dashboard.html in browser</i>"

        return message

    def _format_trade_alert(self, market_name, signal_type, price, indicators):
        """Format trade alert message"""
        emoji = "🟢" if signal_type == "BUY" else "🔴" if signal_type == "SELL" else "🟡"

        message = f"""
{emoji} <b>TRADE SIGNAL: {signal_type}</b>

Market: <b>{market_name}</b>
Price: ${price:,.2f}
Time: {datetime.now().strftime('%H:%M:%S')}

Indicators:
RSI: {indicators.get('RSI', 'N/A')}
MACD: {indicators.get('MACD', 'N/A')}
EMA20: {indicators.get('EMA_20', 'N/A')}
ADX: {indicators.get('ADX', 'N/A')}

<b>Action: {'BUY' if signal_type == 'BUY' else 'SELL' if signal_type == 'SELL' else 'HOLD'}</b>
Risk: 1-2% of capital
"""
        return message


def create_notifier_from_env():
    """Create notifier from environment variables"""
    import os
    from dotenv import load_dotenv

    load_dotenv()

    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not bot_token or not chat_id:
        print("[WARNING] Telegram credentials not configured")
        print("Setup instructions:")
        print("1. Create .env file in project root")
        print("2. Add:")
        print("   TELEGRAM_BOT_TOKEN=your_bot_token")
        print("   TELEGRAM_CHAT_ID=your_chat_id")
        return None

    return TelegramNotifier(bot_token, chat_id)


if __name__ == "__main__":
    # Test notifier
    notifier = create_notifier_from_env()

    if notifier:
        # Test message
        test_markets = {
            'indices': [
                {'name': 'NASDAQ-100', 'symbol': '^IXIC', 'return_pct': 19.81, 'signal': 'BUY'},
                {'name': 'S&P 500', 'symbol': '^GSPC', 'return_pct': 14.79, 'signal': 'SELL'},
            ],
            'commodities': [
                {'name': 'Oil WTI', 'symbol': 'CL=F', 'return_pct': 46.31, 'signal': 'BUY'},
                {'name': 'Gold', 'symbol': 'GC=F', 'return_pct': -4.57, 'signal': 'SELL'},
            ],
            'forex': [
                {'name': 'GBP/USD', 'symbol': 'GBPUSD=X', 'return_pct': 1.44, 'signal': 'SELL'},
            ],
            'crypto': [
                {'name': 'Bitcoin', 'symbol': 'BTC-USD', 'return_pct': -12.04, 'signal': 'BUY'},
            ]
        }

        print("[OK] Sending test summary...")
        notifier.send_market_summary(test_markets)

        print("[OK] Sending test trade alert...")
        indicators = {
            'RSI': 35.5,
            'MACD': -150.23,
            'EMA_20': 6500.00,
            'ADX': 28.5
        }
        notifier.send_trade_alert("NASDAQ-100", "BUY", 22017.85, indicators)
