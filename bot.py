import os
import requests
import feedparser
import urllib.parse
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import schedule
import time

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
RSS_URL = "https://news.google.com/rss/search?q=Poland&hl=en&gl=US&ceid=US:en"

def shorten_url(url):
    api_url = f"http://tinyurl.com/..."
    response = requests.get(api_url)
    return response.text

def send_news():
    feed = feedparser.parse(RSS_URL)
    translator = GoogleTranslator(source='auto', target='ru')
    text = "🇵🇱 Новости Польши:\n\n"
    for entry in feed.entries[:5]:
        title_ru = translator.translate(entry.title)
        short_url = shorten_url(entry.link)
        text += f"• {title_ru}\n{short_url}\n\n"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })
    print("Отправлено")

schedule.every().day.at("08:00").do(send_news)
schedule.every().day.at("12:00").do(send_news)
schedule.every().day.at("18:00").do(send_news)
schedule.every().day.at("21:00").do(send_news)

print("Бот запущен и ждёт времени...")
while True:
    schedule.run_pending()
    time.sleep(60)