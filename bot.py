from telegram.ext import Application, CommandHandler
from user_manager import add_user, update_user_ticker, load_users
from stock import search_for_stock ,fetch_stock_data, calculate_percentage_change
from news import fetch_news
from message import send_message
import os
import asyncio

# Load environment variables
BOT_KEY = os.getenv("BOT_KEY")
STOCKS_API_KEY = os.getenv("STOCKS_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

async def start(update, context):
    """
    Handle the /start command.
    """
    chat_id = update.effective_chat.id
    add_user(chat_id)
    await update.message.reply_text(
        "Welcome to the Stock Tracker Bot! Use /setticker <TICKER> to set the stock ticker you want to track."
    )

async def setticker(update, context):
    """
    Handle the /setticker command to set a stock ticker.
    """
    chat_id = update.effective_chat.id
    if len(context.args) == 0:
        await update.message.reply_text("Please provide a stock ticker. Usage: /setticker <TICKER>\nYou can google the stock ticker of the company if you don't know it.\n US Stocks only !")
        return

    ticker = context.args[0].upper().strip("<>")
    update_user_ticker(chat_id, ticker)
    await update.message.reply_text(f"Stock ticker set to {ticker}.\nYou will now receive updates on market close if your stock had any significant movement.\nHappy Investing!")

async def getticker(update, context):
    """
    Handle the /getticker command to set a stock ticker.
    """
    user = load_users()
    chat_id = update.effective_chat.id
    try:
        ticker = user.get(str(chat_id)).get("ticker")
    except AttributeError:
        ticker = None
    if not ticker:
        await update.message.reply_text("You have not set a stock ticker yet. Use /setticker <TICKER> to set one.")
    else:
        await update.message.reply_text(f"Your stock is {ticker}.")


async def changeticker(update, context):
    """
    Handle the /changeticker command to change the stock ticker.
    """
    await setticker(update, context)

async def notify_users():
    """
    Notify all users of significant stock changes.
    """
    users = load_users()
    bot = Application.builder().token(BOT_KEY).build().bot
    count = 1
    for chat_id, data in users.items():
        ticker = data.get("ticker")
        if not ticker:
            print(ticker)
            continue

        # Fetch stock data and calculate changes
        stock_data = fetch_stock_data(ticker, STOCKS_API_KEY)
        percentage_change = calculate_percentage_change(stock_data)

        if percentage_change and abs(percentage_change) >= 5:
            direction = "🔺" if percentage_change > 0 else "🔻"
            try:
                company_name = search_for_stock(ticker, STOCKS_API_KEY)
            except AttributeError:
                company_name = None
            if not company_name:
                company_name = ticker
            else:
                news = fetch_news(company_name, NEWS_API_KEY)

            # Prepare message
            message = f"The stock {ticker} is {direction} {abs(round(percentage_change))}% today!"
            for article in news:
                message += f"\n\n{article['title']}\n{article['url']}"

            # Send notification
            await send_message(BOT_KEY, chat_id, message)
            print(f"Sent notification to user {count}")
            count += 1

# Initialize the bot application
def create_bot():
    app = Application.builder().token(BOT_KEY).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setticker", setticker))
    app.add_handler(CommandHandler("getticker", getticker))
    app.add_handler(CommandHandler("changeticker", changeticker))
    return app
