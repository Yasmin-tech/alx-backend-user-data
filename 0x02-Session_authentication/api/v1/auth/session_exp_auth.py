#!/usr/bin/env python3
"""
    Create a class that inherits from SessionAuth
    and implement a session expiration mechanism
    """

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
        implement a SessionExpAuth mechanism
        """

    def __init__(self):
        """
            Constructor
            """
        super().__init__()
        session_duration = getenv("SESSION_DURATION")
        try:
            self.session_duration = int(session_duration)
        except TypeError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """
            generate a random session id and add it to the dictionary
            <user_id_by_session_id>
            """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID """
        if session_id is None or not isinstance(session_id, str):
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get("user_id")
        if "created_at" not in session_dictionary:
            return None
        if (datetime.now() - session_dictionary.get("created_at")) > timedelta(
                seconds=self.session_duration):
            return None
        return session_dictionary.get("user_id")
