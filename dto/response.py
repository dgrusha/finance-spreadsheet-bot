from dataclasses import dataclass


@dataclass
class Response:
    is_successful: bool
    message: str
