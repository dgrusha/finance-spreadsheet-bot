from bot import TelegramBot
from utils import check_args
from logging_setup import configure_logger
from logging_setup import logger


if __name__ == "__main__":
    argument = check_args()
    configure_logger(argument.type_of_env)
    bot = TelegramBot()
    logger.info("TelegramBot run...")
    bot.run()
