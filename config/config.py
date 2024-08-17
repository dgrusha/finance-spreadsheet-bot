import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TELEGRAM_ACCESS_TOKEN = os.getenv("TELEGRAM_ACCESS_TOKEN")
    VERSION = os.getenv("VERSION")
    SERVER_SMTP = (os.getenv("SERVER_SMTP"), 465)
    MAIL_SMTP = os.getenv("MAIL_SMTP")
    PASSWORD_SMTP = os.getenv("PASSWORD_SMTP")
    LOGGING_CONFIG = {
        "dev": {
            "console": {
                "level": "INFO",
            },
            "file": {
                "level": "ERROR",
                "filename": os.path.join(ROOT_DIR, "logs", "fsb_dev.log"),
            },
        },
        "prod": {
            "console": {
                "level": "INFO",
            },
            "file": {
                "level": "ERROR",
                "filename": os.path.join(ROOT_DIR, "logs", "fsb_prod.log"),
            },
            "email_report": {
                "level": "ERROR",
                "toaddrs": [
                    os.getenv("ADMIN_EMAIL"),
                ],
                "subject": "Sheet finances - error in telegram bot.",
            },
        },
    }
