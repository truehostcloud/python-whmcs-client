"""This module contains the exceptions raised by Olitt Whmcs."""


class WhmcsException(Exception):
    """An ambiguous exception occurred while performing a whmcs action."""

    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message


class WhmcsConnectionError(WhmcsException):
    """An error occurred while connecting to the whmcs server"""
