import os
from telegram.ext import Application, MessageHandler, filters
from dotenv import load_dotenv

# Load the bot token from .env
load_dotenv()
BOT_KEY = os.getenv("BOT_KEY")

# Function to log the chat ID
async def log_chat_id(update, context):
    chat_id = update.effective_chat.id
    print(f"Chat ID: {chat_id}")

# Initialize the application
app = Application.builder().token(BOT_KEY).build()

# Add the handler
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_chat_id))

# Start polling
print("Send a message to your bot to get your Chat ID")
app.run_polling()

1119308321
