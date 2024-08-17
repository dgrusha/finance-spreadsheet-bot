import argparse
from config import Config


def check_args():
    desc = f"Telegram bot for managing your finances in a spreadsheet - {Config.VERSION}"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--type_of_env",
        help="""Environment can be set to either prod or dev.
         By setting it to prod - all errors will be sent by email to administrators.
         By setting it to dev - all errors will be printed to the console.
        """,
        type=str,
        choices=["prod", "dev"],
        default="dev",
        required=False
    )
    args = parser.parse_args()
    return args
