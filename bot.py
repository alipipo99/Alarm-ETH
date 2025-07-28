import os
import time
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
    except Exception as e:
        print("Failed to send message:", e)

if __name__ == "__main__":
    send_message("🤖 Bot started successfully! ETH/ARB alerts will follow every 6 hours.")
