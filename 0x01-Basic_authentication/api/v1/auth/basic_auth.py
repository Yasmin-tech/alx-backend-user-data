#!/usr/bin/env python3
"""
    Manage user authentication
    """


import base64
import binascii
import re
from api.v1.auth.auth import Auth
from flask import request
from typing import List, TypeVar
from models.user import User


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

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """ Return the user's email and password from the decoded base64
            string decoded_base64_authorization_header
            """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        credentials = re.search(
                r"(.+):(.+)",
                decoded_base64_authorization_header)
        if not credentials:
            return None, None
        return credentials.group(1), credentials.group(2)

    def user_object_from_credentials(
            self, user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """ Return the user object based on the given email and password
        """
        if not user_email or not user_pwd:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        User.load_from_file()
        user_list = User.search({"email": user_email})
        if not user_list or len(user_list) == 0:
            return None
        if not user_list[0].is_valid_password(user_pwd):
            return None
        return user_list[0]
