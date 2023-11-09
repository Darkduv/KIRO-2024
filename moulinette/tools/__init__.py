"""Useful developer tools:
* 'report' to present data
* 'chrono' to time function execution
"""
from .progress import Bar
from .timer import Clock, chrono


def report(title, data, message):
    """Present data in custom message.
    data should be a dictionary, and the message uses any key, value pair.
    """
    print(title)
    if not data:
        print("    Nothing to report")
    for key, value in data.items():
        print("    " + message.format(key=key, value=value))
