import requests
from bs4 import BeautifulSoup
import time

BOT_TOKEN = "PASTE_BOT_TOKEN"
CHAT_ID = "PASTE_CHAT_ID"

URL = "https://chartink.com/dashboard/448209"

sent_stocks = set()

def send_telegram(msg):

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    requests.post(telegram_url, data=payload)

def check_stocks():

    global sent_stocks

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    stocks = []

    for item in soup.find_all("a"):

        text = item.get_text(strip=True)

        if text.isupper() and len(text) < 15:
            stocks.append(text)

    new_stocks = []

    for stock in stocks:

        if stock not in sent_stocks:
            sent_stocks.add(stock)
            new_stocks.append(stock)

    if new_stocks:

        message = "📈 New Stocks:\n\n"

        message += "\n".join(new_stocks)

        send_telegram(message)

        print(message)

while True:

    try:
        check_stocks()

    except Exception as e:
        print(e)

    time.sleep(60)
