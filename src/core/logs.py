import os
import logging
from datetime import datetime, timedelta, timezone

from src.core.settings import settings

# ANSI Color Codes
COLORS = {
    "DEBUG": "\033[94m",     # Blue
    "INFO": "\033[92m",      # Green
    "WARNING": "\033[93m",   # Yellow
    "ERROR": "\033[91m",     # Red
    "CRITICAL": "\033[95m",  # Magenta
    "RESET": "\033[0m"
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = COLORS.get(record.levelname, COLORS["RESET"])
        reset = COLORS["RESET"]

        message = super().format(record)
        return f"{log_color}{message}{reset}"


def ist_time(*args):
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).timetuple()


def log_separator(section_name=None, char="*", line_length=50, spacer_lines=2):
    blank_line = " "
    separator_line = char * line_length

    for _ in range(spacer_lines):
        logger.info(blank_line)

    logger.info(separator_line)
    if section_name:
        logger.info(f"{section_name.center(line_length)}")
        logger.info(separator_line)

    for _ in range(spacer_lines):
        logger.info(blank_line)


def setup_logger():

    logs_format = f"{datetime.now().strftime('%d-%m-%Y')}.log"

    log_file = os.path.join(settings.LOGS_DIR, logs_format)

    debug_mode = str(settings.DEBUG).strip().lower() == "true"
    log_level = logging.DEBUG if debug_mode else logging.INFO

    logger = logging.getLogger()
    logger.setLevel(log_level)

    # avoid duplicate handlers (important for FastAPI reload)
    if logger.hasHandlers():
        logger.handlers.clear()

    # File Handler
    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"
    )
    file_formatter.converter = ist_time
    file_handler.setFormatter(file_formatter)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_formatter = ColoredFormatter(
        "%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"
    )
    console_formatter.converter = ist_time
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Silence noisy logs
    for noisy in [
    "azure",
    "google",
    "google.cloud",
    "google.auth",
    "googleapiclient",
    "urllib3",
    "urllib3.connectionpool",
    "grpc",
    "httpx",
    "httpcore",
    "_client",
]:
        logging.getLogger(noisy).setLevel(logging.ERROR)

    return logger


# Initialize logger
logger = setup_logger()