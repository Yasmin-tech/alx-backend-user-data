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
            Check if the path requires authentication:
            if path is in excluded_paths, this function returns false.
            if path is not in excluded_paths, this function returns true
            """
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True
        else:
            for p in excluded_paths:
                if p.strip("/") == path.strip("/"):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ implement later
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ implement later
        """
        return None
