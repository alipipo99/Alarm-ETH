import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        r = requests.post(url, data=payload)
        r.raise_for_status()
        print("✅ Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print("❌ Failed to send message:", e)
        print("🔎 Check BOT_TOKEN and CHAT_ID environment variables.")

if __name__ == "__main__":
    print("🚀 Starting ETH Alert Bot...")
    print(f"📨 Sending test message to chat ID: {CHAT_ID}")
    message = (
        "👑 *ETH Market Watch Activated*

"
        "✅ *RSI* → 64.2
"
        "📊 *Funding Rate* → +0.017%
"
        "🐋 *Whale Activity* → Moderate inflows

"
        "📤 Alerts sent every 6 hours via Telegram
"
        "_By command of Sultan Ali, the King of Ethereum 👑_"
    )
    send_message(message)
