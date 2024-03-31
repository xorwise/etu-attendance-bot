import re

"""Module for validation"""


def is_valid(email: str) -> bool:
    """Function for email validation

    Args:
        email (str): provided email
    Returns:
        bool: validation result True if email is valid, False otherwise
    """

    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.fullmatch(regex, email)
