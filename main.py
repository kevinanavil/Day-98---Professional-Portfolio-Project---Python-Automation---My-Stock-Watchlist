import requests
from datetime import datetime
import os

########################### Key ###########################
STOCK_NAME = os.getenv("STOCK_NAME")
COMPANY_NAME = os.getenv("COMPANY_NAME")

STOCK_ENDPOINT = os.getenv("STOCK_ENDPOINT")
NEWS_ENDPOINT = os.getenv("NEWS_ENDPOINT")
SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
AUTH = os.getenv("AUTH")

########################### Alpha Vantage ###########################

# Get yesterday's closing stock price
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
#print(yesterday_closing_price)

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
#print(day_before_yesterday_closing_price)

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100, 2)
#print(diff_percent)

########################### News API ###########################

news_params = {
    "apiKey": NEWS_API_KEY,
    "qInTitle": COMPANY_NAME,
}

news_response = requests.get(NEWS_ENDPOINT, params=news_params)
articles = news_response.json()["articles"]

three_articles = articles[:3]

closed = f"{STOCK_NAME}{up_down}{diff_percent}%" 

formatted_articles = [f"- {article['title']}" for article in three_articles]
articles_combined = "\n".join(formatted_articles)

########################### Sheety ###########################

sheety_headers = {
    "Authorization": AUTH,
    "Content-Type": "application/json"
}

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

sheety_params = {
    "sheet1": {
        "date": today_date,
        "time": now_time,
        "closed": closed,
        "article": articles_combined,
        "format": "text-align-vertical: top"
    }
}

response = requests.post(url=SHEETY_ENDPOINT, json=sheety_params, headers=sheety_headers)
print(response.text)