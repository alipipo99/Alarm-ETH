# ETH/ARB Telegram Alert Bot

## Features
- Sends alerts every 6 hours (ETH/ARB RSI, Funding Rate, and Whale Activity)
- Built for deployment on [Railway](https://railway.app)
- Customize `.env` with your bot token and chat ID

## Setup

1. Create a `.env` file with:

```
BOT_TOKEN=your_bot_token
CHAT_ID=your_chat_id
```

2. Run the bot:
```
pip install -r requirements.txt
python bot.py
```
