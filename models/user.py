#!/usr/bin/python3
"""
User class that inherits from BaseModel
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    User class for storing user-related information.
    Attributes:
        email (str): Email of the user, initialized as an empty string.
        password (str): Password of the user, initialized as an empty string.
        first_name (str): First name of the user, initialized as an empty .
        last_name (str): Last name of the user, initialized as an empty string.
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
