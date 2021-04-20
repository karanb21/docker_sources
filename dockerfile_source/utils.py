import logging
from logging.handlers import TimedRotatingFileHandler
import os
import json


def logger(name, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        "%(asctime)s;%(levelname)s;%(message)s", "%Y-%m-%d %H:%M:%S")
    handler = TimedRotatingFileHandler(os.path.join(
        folder, f"{name}.log"), when = "midnight", interval = 1)
    handler.setFormatter(formatter)
    handler.suffix = "%Y%m%d"
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

def parse_config(path):
    with open(path, 'r') as file:
        return json.load(file)
