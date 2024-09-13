#!/usr/bin/env python3
"""
    Hash the password with bcrypt
    """


import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using a random salt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
        Use bcrypt to validate that the provided password
        matches the hashed password
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
