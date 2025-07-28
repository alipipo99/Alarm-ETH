import os
import requests
import numpy as np
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def calculate_rsi_ema(prices, period=14):
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100. / (1. + rs)

    for i in range(period, len(prices)):
        delta = deltas[i - 1]
        upval = max(delta, 0)
        downval = -min(delta, 0)

        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period

        rs = up / down if down != 0 else 0
        rsi[i] = 100. - 100. / (1. + rs)

    return round(rsi[-1], 2)

def fetch_price_and_rsi():
    try:
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": "ETHUSDT", "interval": "4h", "limit": 100}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        closes = [float(entry[4]) for entry in data]

        if len(closes) < 15:
            return "N/A", "N/A"

        rsi = calculate_rsi_ema(np.array(closes))
        return round(closes[-1], 2), rsi
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
    print("🚀 Fetching ETH market data with EMA-based RSI (4H)...")
    price, rsi = fetch_price_and_rsi()
    funding = fetch_funding_rate()
    whale_activity = "Live tracking soon..."

    message = f'''👑 *ETH Market Auto Watch*

💰 *Price:* ${price}
✅ *RSI (4H - EMA):* {rsi}
📊 *Funding Rate:* {funding}%
🐋 *Whale Activity:* {whale_activity}

📤 Alerts sent every 4 hours automatically.
_By order of Sultan Ali, the King of Ethereum 👑_'''
    send_message(message)
