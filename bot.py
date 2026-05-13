import os
import redis
import requests
import feedparser
import urllib.parse
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from groq import Groq
import schedule
import time
import threading

load_dotenv()

TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
REDIS_URL = os.getenv("REDIS_URL")
RSS_URL = "https://news.google.com/rss/search?q=Poland&hl=en&gl=US&ceid=US:en"
RSS_URL2 = "https://notesfrompoland.com/feed"

groq_client = Groq(api_key=GROQ_API_KEY)
r = redis.from_url(REDIS_URL)

def add_subscriber(chat_id):
    r.sadd("subscribers", chat_id)

def load_subscribers():
    return [int(x) for x in r.smembers("subscribers")]

def shorten_url(url):
    api_url = f"http://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}"
    response = requests.get(api_url)
    return response.text

def summarize(title):
    try:
        chat = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": f"Кратко (2-3 предложения) на русском языке опиши о чём эта новость по заголовку: {title}"}]
        )
        return chat.choices[0].message.content
    except:
        return ""

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})

def send_news():
    feed1 = feedparser.parse(RSS_URL)
    feed2 = feedparser.parse(RSS_URL2)
    entries = feed1.entries[:5] + feed2.entries[:5]
    translator = GoogleTranslator(source='auto', target='ru')
    text = "🇵🇱 Новости Польши:\n\n"
    new_entries = []
    for entry in entries:
        if not r.sismember("sent_news", entry.link):
            new_entries.append(entry)
            r.sadd("sent_news", entry.link)
    if not new_entries:
        print("Нет новых новостей")
        return
    for entry in new_entries:
        title_ru = translator.translate(entry.title)
        summary = summarize(entry.title)
        short_url = shorten_url(entry.link)
        text += f"• {title_ru}\n{summary}\n{short_url}\n\n"
    for chat_id in load_subscribers():
        send_message(chat_id, text)
    print("Отправлено")

def check_updates():
    offset = None
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            params = {"timeout": 30}
            if offset:
                params["offset"] = offset
            response = requests.get(url, params=params).json()
            for update in response.get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                text = msg.get("text", "")
                chat_id = msg.get("chat", {}).get("id")
                if text == "/start" and chat_id:
                    add_subscriber(chat_id)
                    send_message(chat_id, "✅ Ты подписан на новости Польши! Новости приходят в 08:00, 12:00 и 18:00.")
        except:
            pass
        time.sleep(1)

threading.Thread(target=check_updates, daemon=True).start()

schedule.every().day.at("06:00").do(send_news)
schedule.every().day.at("10:00").do(send_news)
schedule.every().day.at("16:00").do(send_news)

print("Бот запущен и ждёт времени...")
while True:
    schedule.run_pending()
    time.sleep(60)