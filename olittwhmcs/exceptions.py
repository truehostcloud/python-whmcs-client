"""
This module contains the exceptions raised by Olitt Whmcs.
"""


class WhmcsException(Exception):
    """An ambiguous exception occurred while performing a whmcs action."""

    def __init__(self, message):
        self.message = message


class WhmcsConnectionError(WhmcsException):
    """An error occurred while connecting to the whmcs server"""
