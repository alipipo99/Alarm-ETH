import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def fetch_price_and_rsi():
    try:
        # Fetch 4-hour candles (last 14+1 = 15 needed)
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": "ETHUSDT", "interval": "4h", "limit": 15}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        closes = [float(entry[4]) for entry in data]  # close prices

        if len(closes) < 15:
            return "N/A", "N/A"

        gains = []
        losses = []
        for i in range(1, 15):
            delta = closes[i] - closes[i - 1]
            if delta > 0:
                gains.append(delta)
            else:
                losses.append(abs(delta))
        avg_gain = sum(gains) / 14
        avg_loss = sum(losses) / 14 if losses else 1e-6
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(closes[-1], 2), round(rsi, 2)
    except Exception as e:
        print("❌ Error fetching price/RSI:", e)
        return "N/A", "N/A"

def fetch_funding_rate():
    try:
        url = "https://fapi.binance.com/fapi/v1/premiumIndex?symbol=ETHUSDT"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        rate = float(data["lastFundingRate"]) * 3 * 100
        return round(rate, 4)
    except Exception as e:
        print("❌ Error fetching funding rate:", e)
        return "N/A"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, data=payload, timeout=10)
        r.raise_for_status()
        print("✅ Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print("❌ Failed to send message:", e)

if __name__ == "__main__":
    print("🚀 Fetching ETH market data from Binance (4H candles)...")
    price, rsi = fetch_price_and_rsi()
    funding = fetch_funding_rate()
    whale_activity = "Live tracking soon..."

    message = f'''👑 *ETH Market Auto Watch*

💰 *Price:* ${price}
✅ *RSI (4H):* {rsi}
📊 *Funding Rate:* {funding}%
🐋 *Whale Activity:* {whale_activity}

📤 Alerts sent every 4 hours automatically.
_By order of Sultan Ali, the King of Ethereum 👑_'''
    send_message(message)
