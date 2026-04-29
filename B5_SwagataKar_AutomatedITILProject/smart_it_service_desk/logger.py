import logging
import os

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "logs.txt")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def get_logger(name="ITServiceDesk"):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler - logs everything to logs.txt
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    # Console handler - only INFO and above
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


logger = get_logger()


def log_info(msg):     logger.info(msg)
def log_warning(msg):  logger.warning(msg)
def log_error(msg):    logger.error(msg)
def log_critical(msg): logger.critical(msg)