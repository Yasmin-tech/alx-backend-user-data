#!/usr/bin/env python3
"""
    Manage user authentication
    """


from flask import request
from typing import List, TypeVar


class Auth():
    """
        This class is the template for all authentication
        """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            implement later
            """
        return False

    def authorization_header(self, request=None) -> str:
        """ implement later
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ implement later
        """
        return None
