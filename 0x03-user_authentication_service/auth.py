#!/usr/bin/env python3
"""User Authentecation modle
"""
import bcrypt


from user import Base
from user import User
# from typing import Dict


def _hash_password(password: str) -> bytes:
    """
        Return the salted hash of the input password,
        hashed with bcrypt.hashpw
        """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
