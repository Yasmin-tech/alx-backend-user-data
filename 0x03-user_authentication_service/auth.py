#!/usr/bin/env python3
"""User Authentication modle
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound


from db import DB
from user import Base
from user import User

# from typing import Dict


def _hash_password(password: str) -> bytes:
    """
        Return the salted hash of the input password,
        hashed with bcrypt.hashpw
        """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ initialize an instance of auth
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
            Add the user instance to the database.
            If user already exists, a ValueError is raised
            """
        user_obj = None
        try:
            user_obj = self._db.find_user_by(email=email)
        except NoResultFound:
            pass

        if user_obj is not None:
            raise ValueError("User {} already exists".format(email))
        hashed_pass = _hash_password(password)
        new_user = self._db.add_user(email, hashed_pass)
        return new_user
