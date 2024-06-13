import logging.config
from logging import Logger

logging.config.fileConfig(fname="log.conf")


def get_logger(name: str) -> Logger:
    """Get logger with conf for write logger to console"""
    logger = logging.getLogger(name)
    return logger
