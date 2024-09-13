#!/usr/bin/env python3
"""
    A model contains a function called filter_datum
    that returns the log message obfuscated
    """


import logging
import re
from typing import List
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """
        return a specific logger object
        """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    # Create a handler
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.propagate = False

    # Add the handler to the logger
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a connector to a database.
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection
