#!/usr/bin/env python3
"""
    Create a class that inherits from Auth
    and implement a SessionAuth mechanism
    """


from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
        implement a SessionAuth mechanism
        """
    # a dictionary where key represent session_id and value is the user_id
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
            generate a random session id and add it to the dictionary
            <user_id_by_session_id>
            """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
