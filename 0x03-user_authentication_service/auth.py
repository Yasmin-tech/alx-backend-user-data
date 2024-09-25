#!/usr/bin/env python3
"""User Authentication modle
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


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


def _generate_uuid() -> str:
    """ Return a string representation of a new UUID
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
            Locate the user by email, if it exists and was registered with
            the given password, return True.
            Otherwise, return False
            """
        if not email or not isinstance(email, str):
            return False
        if not password or not isinstance(password, str):
            return False
        user_obj = None

        try:
            user_obj = self._db.find_user_by(email=email)
        except NoResultFound:
            pass

        if user_obj is None:
            return False
        if bcrypt.checkpw(password.encode(), user_obj.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> Union[str, None]:
        """
            Create and return the session id if the user exists.
            Otherwise, return None.
            """
        if not email or not isinstance(email, str):
            return False

        user_obj = None
        try:
            user_obj = self._db.find_user_by(email=email)
        except NoResultFound:
            pass

        if user_obj is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user_obj.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
            Return the use instance if it exists with the given session_id
            """
        if not session_id or isinstance(session_id, str):
            return None

        try:
            user_obj = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user_obj
