import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def fetch_eth_price_and_rsi():
    # Get price history (24h hourly candles) for RSI calculation
    url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart"
    params = {"vs_currency": "usd", "days": "1", "interval": "hourly"}
    response = requests.get(url, params=params)
    data = response.json()
    prices = [price[1] for price in data['prices']]
    if len(prices) < 15:
        return None, None

    # Calculate RSI
    gains = []
    losses = []
    for i in range(1, 15):
        delta = prices[-i] - prices[-i-1]
        if delta >= 0:
            gains.append(delta)
        else:
            losses.append(abs(delta))
    avg_gain = sum(gains) / 14
    avg_loss = sum(losses) / 14
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))

    current_price = prices[-1]
    return round(current_price, 2), round(rsi, 2)

def fetch_funding_rate():
    url = "https://fapi.binance.com/fapi/v1/premiumIndex?symbol=ETHUSDT"
    response = requests.get(url)
    data = response.json()
    rate = float(data["lastFundingRate"]) * 3 * 100  # convert to percent annualized approx
    return round(rate, 4)

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, data=payload)
        r.raise_for_status()
        print("✅ Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print("❌ Failed to send message:", e)

if __name__ == "__main__":
    print("🚀 Fetching ETH market data...")
    price, rsi = fetch_eth_price_and_rsi()
    funding = fetch_funding_rate()
    whale_activity = "Live tracking soon..."

    message = f'''👑 *ETH Market Auto Watch*

💰 *Price:* ${price}
✅ *RSI:* {rsi}
📊 *Funding Rate:* {funding}%
🐋 *Whale Activity:* {whale_activity}

📤 Alerts sent every 6 hours automatically.
_By order of Sultan Ali, the King of Ethereum 👑_'''
    send_message(message)
