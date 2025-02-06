# telegram_bot.py

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from scraper import login_and_scrape
from config import TELEGRAM_BOT_TOKEN

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Define states for the conversation
ORG_CODE, USER_ID, PASSWORD = range(3)

def start(update: Update, context: CallbackContext) -> int:
    logger.info(f"Received /start command from user {update.message.from_user.id}.")
    update.message.reply_text('Welcome! Please provide your ORG Code.')
    return ORG_CODE

def get_org_code(update: Update, context: CallbackContext) -> int:
    context.user_data['org_code'] = update.message.text
    logger.info(f"Received ORG code from user {update.message.from_user.id}.")
    update.message.reply_text('Thanks! Now, please provide your User ID.')
    return USER_ID

def get_user_id(update: Update, context: CallbackContext) -> int:
    context.user_data['user_id'] = update.message.text
    logger.info(f"Received User ID from user {update.message.from_user.id}.")
    update.message.reply_text('Great! Finally, please provide your Password.')
    return PASSWORD

def get_password(update: Update, context: CallbackContext) -> int:
    context.user_data['password'] = update.message.text
    logger.info(f"Received Password from user {update.message.from_user.id}.")

    try:
        logger.info("Starting scraping process...")
        video_urls, pdf_urls = login_and_scrape(
            context.user_data['org_code'],
            context.user_data['user_id'],
            context.user_data['password']
        )
        response = "Video URLs:\n" + "\n".join(video_urls) + "\n\nPDF URLs:\n" + "\n".join(pdf_urls)
        update.message.reply_text(response)
        logger.info("Scraping process completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        update.message.reply_text(f"An error occurred: {e}")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    logger.info(f"Operation cancelled by user {update.message.from_user.id}.")
    update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def main() -> None:
    logger.info("Starting Telegram bot...")
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ORG_CODE: [MessageHandler(Filters.text & ~Filters.command, get_org_code)],
            USER_ID: [MessageHandler(Filters.text & ~Filters.command, get_user_id)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, get_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    logger.info("Bot is running...")
    updater.idle()

if __name__ == '__main__':
    main()
