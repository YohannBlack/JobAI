import logging
import os
import sys
from logging.handlers import RotatingFileHandler


class AppLogger:

    _instances = {}

    DEFAULT_LOG_FORMAT = (
        "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"
    )
    DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    DEFAULT_LOG_LEVEL = logging.INFO

    def __new__(cls, name='app', level=None, log_file=None,
                console_level=None, file_level=None,
                log_format=None, date_format=None,
                max_bytes=10*1024*1024, backup_count=5):

        if name in cls._instances:
            return cls._instances[name]

        instance = super().__new__(cls)
        cls._instances[name] = instance
        instance._initialized = False
        return instance

    def __init__(self, name='app', level=None, log_file=None,
                 console_level=None, file_level=None,
                 log_format=None, date_format=None,
                 max_bytes=10*1024*1024, backup_count=5):
        if self._initialized:
            return
        self._initialized = True

        self.name = name
        self.logger = logging.getLogger(name)

        _overall_level = level if level is not None else self.DEFAULT_LEVEL
        _console_level = console_level if console_level is not None else _overall_level
        _file_level = file_level if file_level is not None else _overall_level

        effective_logger_level = min(_console_level, _file_level if log_file else _console_level)
        if log_file:
             effective_logger_level = min(effective_logger_level, _file_level)

        self.logger.setLevel(effective_logger_level)

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        _log_format = log_format if log_format else self.DEFAULT_LOG_FORMAT
        _date_format = date_format if date_format else self.DEFAULT_DATE_FORMAT
        formatter = logging.Formatter(_log_format, datefmt=_date_format)

        if _console_level is not None:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(_console_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        if log_file:
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(_file_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        if self.logger.hasHandlers():
            self.logger.propagate = False

    def debug(self, message, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self.logger.critical(message, *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        self.logger.exception(message, *args, **kwargs)

    def get_logger(self):
        return self.logger