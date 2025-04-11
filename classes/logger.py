from datetime import datetime
import logging
import os
from logging.handlers import RotatingFileHandler
from colorama import init, Fore, Style

init(autoreset=True)


class ColorFormatter(logging.Formatter):
    COLOR_MAP = {
        logging.DEBUG: Style.DIM + Fore.WHITE,               # Серый (тусклый)
        logging.INFO: Style.DIM + Fore.WHITE,                # Серый
        logging.WARNING: Style.BRIGHT + Fore.YELLOW,         # Жёлтый
        logging.ERROR: Style.BRIGHT + Fore.LIGHTRED_EX,      # Светло-красный
        logging.CRITICAL: Style.BRIGHT + Fore.RED,           # Буро-красный
    }

    def format(self, record):
        color = self.COLOR_MAP.get(record.levelno, "")
        message = super().format(record)
        return color + message + Style.RESET_ALL


class Logger:
    def __init__(self, name="ROOT", log_dir="logs", level=logging.DEBUG, max_bytes=1_000_000, backup_count=3):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False

        if not self.logger.handlers:
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, f"{name}.log")


            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_filename = f"{name}_{timestamp}.log"
            log_path = os.path.join(log_dir, log_filename)

            file_handler = RotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8')
            file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            color_formatter = ColorFormatter('[%(levelname)s] %(message)s')
            console_handler.setFormatter(color_formatter)
            self.logger.addHandler(console_handler)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)
