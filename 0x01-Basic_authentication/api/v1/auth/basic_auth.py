#!/usr/bin/env python3
"""
    Manage user authentication
    """


from api.v1.auth.auth import Auth
from flask import request
from typing import List, TypeVar


class BasicAuth(Auth):
    """
        Inherits from Auth and implement BasicAuth mechanesim
        """
