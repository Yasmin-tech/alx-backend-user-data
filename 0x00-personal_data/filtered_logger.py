#!/usr/bin/env python3
"""
    A model contains a function called filter_datum
    that returns the log message obfuscated
    """


import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
        a function called filter_datum that returns the log message obfuscated
        """
    for field in fields:
        message = re.sub(
                "{}=.*?{}".format(field, separator),
                field + "=" + redaction + separator,
                message)

    return message
