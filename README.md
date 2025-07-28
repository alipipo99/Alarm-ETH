# Fixed ETH Alert Telegram Bot

## ✅ Description
This version includes error handling and prints debug info to Railway logs if message sending fails.

## 🛠 Setup
1. Create `.env` file:
```
BOT_TOKEN=7687238301:AAGXMxVR4EDlR284kM4SdDCoEtPZoIMVZb8
CHAT_ID=1002836287330
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the bot:
```
python bot.py
```

If no message arrives in Telegram, check the Railway logs for errors!
