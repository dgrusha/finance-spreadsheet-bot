import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TELEGRAM_ACCESS_TOKEN = os.getenv('TELEGRAM_ACCESS_TOKEN')
