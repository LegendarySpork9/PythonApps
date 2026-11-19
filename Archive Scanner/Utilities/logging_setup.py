import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(log_dir: str):
    logger = logging.getLogger("archive_scanner")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(module)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    log_path = os.path.join(log_dir, "scanner.log")
    file_handler = RotatingFileHandler(
        log_path, maxBytes=1_048_576, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
