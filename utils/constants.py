from enum import Enum


class State(Enum):
    BASIC = 1
    SEND_EMAIL = 2


WELCOME_TEXT: str = "Welcome! Use /description to get started."
HANDLE_MESSAGE_OTHER_TEXT: str = (
    "I am not currently waiting for any input. "
    "Maybe you want to use one of the commands? Use /description to choose one."
)
UNKNOWN_ERROR: str = "Unknown error has appeared."

USER_STRUCTURE_MONGO: dict = {
    "user_id": "",
    "verified": False,
    "email": "",
    "spreadsheet_link": "",
}

EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
