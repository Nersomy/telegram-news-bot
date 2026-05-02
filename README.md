# 🇵🇱 Telegram News Bot

![Python](https://img.shields.io/badge/Python-3-blue) ![Railway](https://img.shields.io/badge/Hosted-Railway-green) ![Telegram](https://img.shields.io/badge/Telegram-Bot-blue)

A bot that automatically sends the latest news about Poland to Telegram twice a day. News is fetched from Google News RSS and translated into Russian.

## Features

- Fetches news from Google News RSS
- Automatically translates headlines into Russian
- Sends top 5 news at 08:00 and 18:00
- Short links via TinyURL
- Hosted on Railway

## Stack

- `feedparser` — RSS parsing
- `deep-translator` — translation via Google Translate
- `schedule` — sending schedule
- `python-dotenv` — token storage

## Installation

```bash
git clone https://github.com/Nersomy/telegram-news-bot.git
cd telegram-news-bot
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```
TOKEN=your_bot_token
CHAT_ID=your_chat_id
```

## Run

```bash
python bot.py
```

## Deploy

The project is deployed on **Railway**. Every push to `main` triggers an automatic deploy.
