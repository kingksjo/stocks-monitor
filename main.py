import asyncio
from bot import create_bot, notify_users
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
import os

def schedule_notifications():
    """
    Schedule daily notifications at 9 PM UTC using APScheduler.
    """
    scheduler = BackgroundScheduler()

    # Schedule the notification function to run every weekday at 9 PM UTC
    scheduler.add_job(
        func=lambda: asyncio.run(notify_users()),
        trigger="cron",
        day_of_week="mon-fri",
        hour=21,  # 9 PM UTC
        minute=2,
        second=0,
    )

    scheduler.start()
    print("Notification scheduling started...")

def main():
    """
    Entry point for the application.
    """
    # Create and start the Telegram bot
    bot_app = create_bot()

    # Schedule daily notifications
    schedule_notifications()

    # Start the bot (this will block the current thread)
    print(f"Bot started at {datetime.now()}")
    bot_app.run_polling()

if __name__ == "__main__":
    main()
