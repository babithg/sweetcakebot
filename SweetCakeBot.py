#!/usr/bin/env python

import logging, json, requests, time, re

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logger.info(f"Chatting with {user.full_name} ID: {user.id}")
    message = f"Hey {user.mention_html()} ! \nHow are you ?"
    await update.message.reply_html(message, reply_markup=ForceReply(selective=True),)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help ?\nJust type you will come to know :)")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(f"Got your message : {update.message.text}")


async def address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List of Address of cakes."""
    await update.message.reply_text("1. Calicut \n2. Kannur \n3. Bengalore")

def get_joke():
    data = requests.get(url="https://official-joke-api.appspot.com/random_joke")
    setup = data.json()['setup']
    punchline = data.json()['punchline']
    return (setup, punchline)

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get a Random joke."""
    new_joke = get_joke()
    await update.message.reply_text(new_joke[0])
    time.sleep(5)
    await update.message.reply_text(new_joke[1])

def get_age(name):
    data = requests.get(url="https://api.agify.io/?name=" + name)
    return data.json()['age']

async def guess_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Guess age of the user"""
    await update.message.reply_text("Tell me your name ?")
    time.sleep(5)
    age = get_age(update.message.text)
    await update.message.reply_text(f"{update.message.from_user.first_name} age around {age}")


async def cakelist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List of Cakes to user"""

    await update.message.reply_text("1. Black Forest \n2. White Forest \n3.Chocolate \n4.Eggless Cake \n5. Special Cake \nWhich one are you looking to buy?")


def main() -> None:

    TOKEN = None
    # Read Token from the data file
    with open('data.sec', 'r') as f:
        TOKEN = json.loads(f.read())
    
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN['value']).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cakelist", cakelist))
    application.add_handler(CommandHandler("address", address))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.Regex("(joke|Joke)"), joke))
    application.add_handler(MessageHandler(filters.Regex(re.compile(r"(?i).*\bguess\s*my\s*age\b.*",re.IGNORECASE)), guess_age))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()