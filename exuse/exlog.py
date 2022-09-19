import sys
import logging


def log_error_and_exit(msg: str):
    """log an error message and exit the process"""
    logging.error(msg)
    sys.exit()

def log_error_and_raise(msg: str, exception: Exception):
    logging.error(msg)
    raise exception