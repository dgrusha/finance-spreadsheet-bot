from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from config import Config
from logging_setup import logger


class TelegramBot:
    def __init__(self):
        logger.info("TelegramBot initialization started.")
        self.application = (
            ApplicationBuilder().token(Config.TELEGRAM_ACCESS_TOKEN).build()
        )

        # Handlers
        self.application.add_handler(CommandHandler("test", self.test))
        logger.info("TelegramBot initialization finished.")

    async def test(self, update: Update, context: ContextTypes):
        user = update.message.from_user
        logger.info(f"{user.id} -- {user.username}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Hello! I am your bot."
        )

    def run(self):
        self.application.run_polling()
