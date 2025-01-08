import asyncio
from telegram import Bot

async def send_message(bot_token, chat_id, message):
    """
    Send a message to a specific Telegram chat.

    Args:
        bot_token (str): Telegram bot token.
        chat_id (int): Chat ID of the recipient.
        message (str): The message content.

    Returns:
        None
    """
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

async def send_notifications(bot_token, notifications):
    """
    Send notifications to multiple users.

    Args:
        bot_token (str): Telegram bot token.
        notifications (list): List of tuples [(chat_id, message), ...]

    Returns:
        None
    """
    bot = Bot(token=bot_token)
    for chat_id, message in notifications:
        await bot.send_message(chat_id=chat_id, text=message)
