from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from config import Config
from logging_setup import logger
import os
from services.redis_client import redis_db
from utils.constants import State, WELCOME_TEXT, HANDLE_MESSAGE_OTHER_TEXT
from dto.response import Response
from bot.bot_handlers import save_email_for_user, get_user_record_by_id


class TelegramBot:
    """
    A class to represent the Telegram bot, managing command handlers and message responses.
    """

    def __init__(self):
        """
        Initializes the TelegramBot class, setting up command and message handlers.
        """
        logger.info("TelegramBot initialization started.")
        self.application = (
            ApplicationBuilder().token(Config.TELEGRAM_ACCESS_TOKEN).build()
        )

        # CommandHandlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("description", self.description))
        self.application.add_handler(CommandHandler("enter_email", self.enter_email))
        self.application.add_handler(
            CommandHandler("get_active_email", self.get_active_email)
        )

        # MessageHandlers
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message)
        )

        logger.info("TelegramBot initialization finished.")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles the /start command. Sets the user's status in Redis and sends a welcome message.

        Args:
            update (Update): The update object containing information about the incoming update.
            context (ContextTypes.DEFAULT_TYPE): The context object providing access to bot data.
        """
        user = update.message.from_user
        logger.info(f"{user.id} -- {user.username}")
        redis_db.set_with_prefix(user.id, State.BASIC.value, "status")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=WELCOME_TEXT
        )

    async def description(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles the /description command. Sends an HTML formatted description of the bot.

        Args:
            update (Update): The update object containing information about the incoming update.
            context (ContextTypes.DEFAULT_TYPE): The context object providing access to bot data.
        """
        user = update.message.from_user
        chat_id = update.effective_chat.id
        redis_db.set_with_prefix(user.id, State.BASIC.value, "status")

        with open(
            os.path.join(Config.ROOT_DIR, "html", "description.html"), "r"
        ) as file:
            html_content = file.read()

        await context.bot.send_message(
            chat_id=chat_id, text=html_content, parse_mode="HTML"
        )

    async def enter_email(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles the /enter_email command. Prompts the user to enter their email address.

        Args:
            update (Update): The update object containing information about the incoming update.
            context (ContextTypes.DEFAULT_TYPE): The context object providing access to bot data.
        """
        user_id: int = update.message.from_user.id
        redis_db.set_with_prefix(user_id, State.SEND_EMAIL.value, "status")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please send your email address in the next message.",
        )

    async def get_active_email(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """
        Handles the /get_active_email command. Retrieves and sends the user's active email address.

        Args:
            update (Update): The update object containing information about the incoming update.
            context (ContextTypes.DEFAULT_TYPE): The context object providing access to bot data.
        """
        user_id: int = update.message.from_user.id
        redis_db.set_with_prefix(user_id, State.BASIC.value, "status")
        user = get_user_record_by_id(user_id)
        if not user:
            message = "You have no active email address."
        else:
            user_email: str = user.get("email")
            if not user_email:
                message = "You have no active email address."
            else:
                message = f"Your active email address is: {user.get('email')}"
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"{message}"
        )

    async def handle_text_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """
        Handles all text messages that are not commands. Saves the email if the user is in the SEND_EMAIL state,
        otherwise sends a generic response.

        Args:
            update (Update): The update object containing information about the incoming update.
            context (ContextTypes.DEFAULT_TYPE): The context object providing access to bot data.
        """
        user_id: int = update.message.from_user.id
        status = int(redis_db.get_with_prefix(user_id, "status").decode("utf-8"))

        if status and status == State.SEND_EMAIL.value:
            response: Response = save_email_for_user(user_id, update.message.text)
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"{response.message}"
            )
            redis_db.set_with_prefix(user_id, State.BASIC.value, "status")
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=HANDLE_MESSAGE_OTHER_TEXT
            )

    def run(self):
        self.application.run_polling()
