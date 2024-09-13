#!/usr/bin/env python3
"""
    Hash the password with bcrypt
    """


import bcrypt


def hash_password(password):
    """
        Hash the password with bcrypt
        """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
