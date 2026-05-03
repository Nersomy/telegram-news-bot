import os
import requests
import feedparser
import urllib.parse
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from groq import Groq
import schedule
import time

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
RSS_URL = "https://news.google.com/rss/search?q=Poland&hl=en&gl=US&ceid=US:en"
RSS_URL2 = "https://notesfrompoland.com/feed"

groq_client = Groq(api_key=GROQ_API_KEY)

def shorten_url(url):
    api_url = f"http://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}"
    response = requests.get(api_url)
    return response.text

def summarize(title, link):
    try:
        chat = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": f"Кратко (2-3 предложения) на русском языке опиши о чём эта новость по заголовку: {title}"}]
        )
        return chat.choices[0].message.content
    except:
        return ""

def send_news():
    feed1 = feedparser.parse(RSS_URL)
    feed2 = feedparser.parse(RSS_URL2)
    entries = feed1.entries[:5] + feed2.entries[:5]
    translator = GoogleTranslator(source='auto', target='ru')
    text = "🇵🇱 Новости Польши:\n\n"
    for entry in entries:
        title_ru = translator.translate(entry.title)
        summary = summarize(entry.title, entry.link)
        short_url = shorten_url(entry.link)
        text += f"• {title_ru}\n{summary}\n{short_url}\n\n"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    print("Отправлено")

schedule.every().day.at("08:00").do(send_news)
schedule.every().day.at("12:00").do(send_news)
schedule.every().day.at("18:00").do(send_news)

print("Бот запущен и ждёт времени...")
while True:
    schedule.run_pending()
    time.sleep(60)