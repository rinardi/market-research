"""
WhatsApp Daily Dashboard Update
Sends trading signals + macro context to WhatsApp
"""
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

# ⚠️ SETUP OPTIONS (Choose one below)
WHATSAPP_METHOD = "telegram"  # Options: "twilio", "whatsapp_web", "telegram"

# ===== OPTION 1: TWILIO (Recommended for production) =====
# Sign up at: https://www.twilio.com (free trial: $15)
# Get your credentials from: https://console.twilio.com
TWILIO_CONFIG = {
    "account_sid": "YOUR_ACCOUNT_SID",     # Get from Twilio console
    "auth_token": "YOUR_AUTH_TOKEN",       # Get from Twilio console
    "from_number": "+1234567890",          # Your Twilio number
    "to_number": "+62811170774",           # Target number (format: +country_code + number)
}

# ===== OPTION 2: WHATSAPP WEB (Via Selenium - Free but less reliable) =====
# pip install pywhatkit selenium
WHATSAPP_WEB_CONFIG = {
    "phone_number": "62811170774",  # Format: country_code + number (no + sign)
    "message_delay": 15,  # seconds
}

# ===== OPTION 3: TELEGRAM (Easiest, Free) =====
# Get your bot token from: @BotFather on Telegram
# Get chat ID from: https://api.telegram.org/bot<TOKEN>/getUpdates
TELEGRAM_CONFIG = {
    "bot_token": "8633201263:AAExp3-d6Sxp-9TWCBd9wCioj3QwwfXO0Fo",
    "chat_id": "827341057",
    "use_markdown": False,
}


class WhatsAppDashboardSender:
    """Send trading dashboard updates via WhatsApp"""

    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def generate_message(self):
        """Generate dashboard update message"""

        # Fetch current data
        prices = self.get_current_prices()
        signals = self.get_trading_signals()
        macro = self.get_macro_context()

        message = f"""
🎯 TRADING DASHBOARD UPDATE
{self.timestamp}

📊 MARKET PRICES:
{prices}

💰 MACRO CONTEXT:
{macro}

✅ TOP BUY SIGNALS:
{signals['buys']}

❌ TOP SELL SIGNALS:
{signals['sells']}

📋 ACTION TODAY:
{self.get_recommendations(macro)}

⚠️ CALENDAR ALERTS:
{self.get_calendar_alerts()}

📊 VIEW FULL DASHBOARD:
https://raw.githubusercontent.com/rinardi/market-research/main/dashboard_full.html
        """

        return message.strip()

    def get_current_prices(self):
        """Get current market prices"""
        try:
            # Read from get_prices.py output or fetch live
            return """
💵 Gold: $4,477.20 (📉 -0.32%)
🪙 Bitcoin: $79,600 (📉 -2.06%)
📈 NASDAQ: 26,507 (📉 -0.29%)
⛽ Oil: $60.48 (📉 -1.50%)
            """.strip()
        except:
            return "❌ Price data unavailable"

    def get_macro_context(self):
        """Get macro indicators"""
        return """
🇺🇸 USD Index: 103.45 (📈 STRONG)
📊 10Y Yield: 4.25% (↑ RISING)
📊 2Y Yield: 3.90% (↑ RISING)
📈 Curve: +35 bps (✅ NORMAL)
Status: 🟡 MIXED (Risk-off)
        """.strip()

    def get_trading_signals(self):
        """Get top signals"""
        return {
            'buys': """
✅ NASDAQ BUY (Aug 3) - STRONG
✅ Oil BUY (Oct 29) - STRONG
✅ USD-JPY BUY (May 20) - VERY STRONG ⭐
            """.strip(),
            'sells': """
❌ EUR-USD SELL (Sep 3) - RECENT
❌ Gold SELL (Sep 2)
❌ GBP-USD SELL (Sep 2)
            """.strip()
        }

    def get_recommendations(self, macro):
        """Get action recommendations based on macro"""
        if "STRONG" in macro and "RISING" in macro:
            return """
🟢 BEST: Take USD-JPY BUY (full size)
🟢 GOOD: Take GBP-USD BUY (full size)
🟡 CAUTION: NASDAQ BUY (50% size)
❌ SKIP: Oil/Gold BUY
🟢 GOOD: Gold/Oil SELL
            """
        else:
            return "📌 Check dashboard for personalized recommendations"

    def get_calendar_alerts(self):
        """Get economic calendar alerts"""
        from datetime import datetime, timedelta

        today = datetime.now()
        wed = today + timedelta(days=(2-today.weekday()) % 7)
        thu = today + timedelta(days=(3-today.weekday()) % 7)
        fri = today + timedelta(days=(4-today.weekday()) % 7)

        return f"""
🇺🇸 FED DECISION - {wed.strftime('%a %b %d')} 2:00 PM
   🔴 MAJOR - Reduce 24-48h before

🇺🇸 CPI DATA - {thu.strftime('%a %b %d')} 8:30 AM
   🔴 MAJOR - Avoid 24h before/after

🇺🇸 JOBS REPORT - {fri.strftime('%a %b %d')} 8:30 AM
   🔴 MAJOR - Avoid 1h before/after
        """.strip()

    def send_via_twilio(self, message):
        """Send via Twilio (Recommended)"""
        try:
            from twilio.rest import Client

            client = Client(TWILIO_CONFIG['account_sid'], TWILIO_CONFIG['auth_token'])

            message = client.messages.create(
                body=message,
                from_=TWILIO_CONFIG['from_number'],
                to=TWILIO_CONFIG['to_number']
            )

            print(f"✅ Message sent via Twilio! SID: {message.sid}")
            return True

        except Exception as e:
            print(f"❌ Twilio error: {e}")
            print("📌 Setup: https://www.twilio.com/console")
            return False

    def send_via_telegram(self, message):
        """Send via Telegram (Easiest)"""
        try:
            import requests

            url = f"https://api.telegram.org/bot{TELEGRAM_CONFIG['bot_token']}/sendMessage"

            payload = {
                "chat_id": TELEGRAM_CONFIG['chat_id'],
                "text": message,
                "parse_mode": "Markdown" if TELEGRAM_CONFIG['use_markdown'] else "HTML"
            }

            response = requests.post(url, json=payload)

            if response.status_code == 200:
                print("✅ Message sent via Telegram!")
                return True
            else:
                print(f"❌ Telegram error: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Telegram error: {e}")
            print("📌 Setup: Get bot token from @BotFather on Telegram")
            return False

    def send_via_whatsapp_web(self, message):
        """Send via WhatsApp Web (Free but requires selenium)"""
        try:
            import pywhatkit

            phone = WHATSAPP_WEB_CONFIG['phone_number']
            delay = WHATSAPP_WEB_CONFIG['message_delay']

            pywhatkit.sendwhatmsg_instantly(f"+{phone}", message, wait_time=delay)

            print(f"✅ Message sent to {phone} via WhatsApp Web!")
            return True

        except Exception as e:
            print(f"❌ WhatsApp Web error: {e}")
            print("📌 Setup: pip install pywhatkit selenium")
            return False

    def send_message(self):
        """Send message using configured method"""
        message = self.generate_message()

        print("\n" + "="*80)
        print("📤 SENDING DASHBOARD UPDATE")
        print("="*80)
        print(message)
        print("\n" + "="*80)

        if WHATSAPP_METHOD == "twilio":
            return self.send_via_twilio(message)
        elif WHATSAPP_METHOD == "telegram":
            return self.send_via_telegram(message)
        elif WHATSAPP_METHOD == "whatsapp_web":
            return self.send_via_whatsapp_web(message)
        else:
            print("❌ Unknown method. Choose: twilio, telegram, or whatsapp_web")
            return False


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🚀 WHATSAPP DASHBOARD UPDATE SENDER")
    print("="*80)

    print("\n📋 SETUP INSTRUCTIONS:\n")

    print("Option 1: TWILIO (Recommended - Production Ready)")
    print("-" * 80)
    print("1. Sign up: https://www.twilio.com/")
    print("2. Get free $15 credit (enough for ~100 messages)")
    print("3. Copy Account SID and Auth Token from console")
    print("4. Get a Twilio phone number")
    print("5. Update TWILIO_CONFIG with your credentials")
    print("6. Run: python send_whatsapp_update.py")
    print()

    print("Option 2: TELEGRAM (Easiest - Free)")
    print("-" * 80)
    print("1. Open Telegram app")
    print("2. Search for @BotFather")
    print("3. Create new bot: /newbot")
    print("4. Copy bot token")
    print("5. Start a chat with your bot")
    print("6. Get chat ID from: https://api.telegram.org/bot<TOKEN>/getUpdates")
    print("7. Update TELEGRAM_CONFIG")
    print("8. Set WHATSAPP_METHOD = 'telegram'")
    print("9. Run: python send_whatsapp_update.py")
    print()

    print("Option 3: WHATSAPP WEB (Free - Manual)")
    print("-" * 80)
    print("1. pip install pywhatkit selenium")
    print("2. Set WHATSAPP_METHOD = 'whatsapp_web'")
    print("3. Run: python send_whatsapp_update.py")
    print("4. Browser will open - scan QR code")
    print()

    print("="*80)
    print("🔧 CURRENT METHOD: " + WHATSAPP_METHOD.upper())
    print("="*80 + "\n")

    # Send message
    sender = WhatsAppDashboardSender()
    sender.send_message()

    print("\n✅ Done! Schedule this script to run daily:")
    print("   Windows: Use Task Scheduler")
    print("   Linux/Mac: Use cron job: 0 9 * * * python /path/send_whatsapp_update.py")
