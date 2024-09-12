#!/usr/bin/env python3
"""
    A model contains a function called filter_datum
    that returns the log message obfuscated
    """


import logging
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
            format the message
            """
        message = filter_datum(
                self.fields,
                self.REDACTION,
                record.msg,
                self.SEPARATOR)
        record.msg = message  # Update the message in the record
        return super(RedactingFormatter, self).format(record)
