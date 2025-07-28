# Fixed ETH Alert Telegram Bot

## ✅ Description
This version includes error handling and prints debug info to Railway logs if message sending fails.

## 🛠 Setup
1. Create `.env` file:
```
BOT_TOKEN=your_bot_token
CHAT_ID=your_chat_id
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
