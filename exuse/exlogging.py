# coding=utf-8

import sys
import logging


def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )


def log_error_and_exit(msg: str):
    """log an error message and exit the process"""
    logging.error(msg)
    sys.exit()


def log_error_and_raise(msg: str, exception: Exception):
    logging.error(msg)
    raise exception
