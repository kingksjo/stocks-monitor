import requests
import os
from dotenv import load_dotenv
from message import send_message
import asyncio


load_dotenv()



def high_activity(percentage):
    if percentage >= 5:
        return "up" # f"🔺{STOCK} is above {round(percentage)}"
    elif percentage <= -5:
        return "down" # f"🔻{STOCK} is below {round(percentage)}"
    

def check_news(news_url, news_parameters, percentage):
    news_response = requests.get(news_url, params=news_parameters)
    news_response.raise_for_status()

    news_data = news_response.json()

    for i in news_data["articles"]:
        if percentage >= 5:
            asyncio.run(send_message(bot_token=os.getenv("BOT_KEY"), chat_id="",message=f"🔺 {stock} is up {round(percentage)}\n{i["title"]}\n{i["content"]}\n{i["source"]["name"]}\n{i["url"]}"))
            print(
                f"🔺 {stock} is up {round(percentage)}\n{i["title"]}\n{i["content"]}\n{i["source"]["name"]}\n{i["url"]}"
            )
        elif percentage <= -5:
            asyncio.run(send_message(bot_token=os.getenv("BOT_KEY"), chat_id="",message=f"🔻 {stock} is up {round(percentage)}\n{i["title"]}\n{i["content"]}\n{i["source"]["name"]}\n{i["url"]}"))
            print(
                f"🔻 {stock} is down {round(percentage)}\n{i["title"]}\n{i["content"]}\n{i["source"]["name"]}\n{i["url"]}"
            )


stock = "CRWD"
company_name = "CrowdStrike Holdings, Inc."

print(stock)
print(company_name)

stocks_url = "https://www.alphavantage.co/query"
stock_api_key = os.getenv("STOCKS_API_KEY")

news_url = "https://newsapi.org/v2/everything"
news_api_key = os.getenv("NEWS_API_KEY")

news_parameters = {
    "q": company_name,
    "pageSize": 3,
    "apiKey": news_api_key
}

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": stock,
    "apikey": stock_api_key
}

stocks_response = requests.get(stocks_url, params=stock_parameters)
stocks_response.raise_for_status()

data = stocks_response.json()

current, previous = list(data["Time Series (Daily)"].keys())[0], list(data["Time Series (Daily)"].keys())[1]

closing_prices = (float(data["Time Series (Daily)"][current]["4. close"]), float(data["Time Series (Daily)"][previous]["4. close"]))

percentage = ((closing_prices[0] - closing_prices[1]) / closing_prices[1]) * 100


if high_activity(percentage) == "up" or high_activity(percentage) == "down":
    check_news(news_url, news_parameters, percentage)

# Percentage increase is ((high - open) / open * 100 )
# percentage decrease is ((low - open) /  open * 100 )

# percentage is today - yesterday / yesterday * 100

# for the data in time series daily, save todays data and yesterdays data in a tuple





