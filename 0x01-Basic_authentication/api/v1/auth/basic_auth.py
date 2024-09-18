#!/usr/bin/env python3
"""
    Manage user authentication
    """


import base64
import binascii
from api.v1.auth.auth import Auth
from flask import request
from typing import List, TypeVar


class BasicAuth(Auth):
    """
        Inherits from Auth and implement BasicAuth mechanesim
        """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """ Return the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        # if the authorization_header starts with "Basic "
        # we should retuen what is after it from index 6
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
            Return the decoded value of a Base64 string
            base64_authorization_header
            """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_decoded = base64.b64decode(base64_authorization_header)
        except binascii.Error:
            return None
        return base64_decoded.decode("utf-8")
