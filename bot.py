import requests
import feedparser
from deep_translator import GoogleTranslator
import schedule
import time

TOKEN = "8604218561:AAGwQVmEpiFlK8Xcvut3vsc4x2QllSp5P7U"
CHAT_ID = "8421007638"

RSS_URL = "https://news.google.com/rss/search?q=Poland&hl=en&gl=US&ceid=US:en"

def send_news():
    feed = feedparser.parse(RSS_URL)
    translator = GoogleTranslator(source='auto', target='ru')

    text = "🇵🇱 Новости Польши:\n\n"

    for entry in feed.entries[:5]:
        title_ru = translator.translate(entry.title)
        text += title_ru + "\n" + entry.link + "\n\n"

    url = f"https://api.telegram.org/bot8604218561:AAGwQVmEpiFlK8Xcvut3vsc4x2QllSp5P7U/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("Отправлено")

# ⏰ расписание
schedule.every().day.at("08:00").do(send_news)
schedule.every().day.at("18:00").do(send_news)

print("Бот запущен и ждёт времени...")

while True:
    schedule.run_pending()
    time.sleep(60)