from services.mongo_db_client import mongo_db
from utils.constants import USER_STRUCTURE_MONGO, EMAIL_PATTERN
from dto.response import Response
from logging_setup import logger
import re
from typing import Any


def save_email_for_user(user_id: int, email: str) -> Response:
    """
    Saves the provided email address for a user in the MongoDB database.

    Args:
        user_id (int): The unique identifier of the user.
        email (str): The email address to be saved.

    Returns:
        Response: An object containing a message and a success status.
    """
    try:
        if not user_id:
            return Response(
                message="UserId is should be provided.", is_successful=False
            )
        if not email:
            return Response(message="Email is should be provided.", is_successful=False)
        if email and re.match(EMAIL_PATTERN, email) is None:
            return Response(
                message="Email is provided does not match email pattern.",
                is_successful=False,
            )

        user_record = get_user_record_by_id(user_id)
        user_structure: dict = USER_STRUCTURE_MONGO

        if not user_record:
            user_structure["email"] = email
            user_structure["user_id"] = user_id
            mongo_db.insert_document("users", user_structure)
        else:
            mongo_db.update_document("users", {"user_id": user_id}, {"email": email})

        return Response(message="Email was saved successfully.", is_successful=True)
    except Exception as e:
        logger.exception(repr(e))
        return Response(message="Unknown error has appeared.", is_successful=False)


def get_user_record_by_id(user_id: int) -> Any:
    """
    Retrieves a user record from the MongoDB database by user ID.

    Args:
        user_id (int): The unique identifier of the user.

    Returns:
        Any: The user record if found, otherwise `None`.
    """
    return mongo_db.find_one_document("users", {"user_id": user_id})
