"""DEBUG, INFO, WARNING, ERROR и CRITICAL"""
import logging
import logging.config

DEBUG = True
from logging_config import LOGGING_CONF

if __name__ == '__main__':
    print(type(LOGGING_CONF))