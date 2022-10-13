from functools import wraps
import logging
import logging.config
import os
import sys
from types import FunctionType

import yaml


class DefaultLogger:
    """Default logging Class that can be used for static logging."""

    initialized = False

    @staticmethod
    def log(*args, **kwargs):
        """Static generic log."""
        return logging.getLogger(sys._getframe(1).f_code.co_name).log(*args, **kwargs)

    @staticmethod
    def info(*args, **kwargs):
        """Static info log."""
        return logging.getLogger(sys._getframe(1).f_code.co_name).info(*args, **kwargs)

    @staticmethod
    def debug(*args, **kwargs):
        """Static debug log."""
        return logging.getLogger(sys._getframe(1).f_code.co_name).debug(*args, **kwargs)

    @staticmethod
    def warning(*args, **kwargs):
        """Static warning log."""
        return logging.getLogger(sys._getframe(1).f_code.co_name).warning(*args, **kwargs)

    @staticmethod
    def error(*args, **kwargs):
        """Static error log."""
        return logging.getLogger(sys._getframe(1).f_code.co_name).error(*args, **kwargs)

    @classmethod
    def setup_logging(
        cls,
        default_path: str = "logging.yaml",
        default_level: int = logging.INFO,
        env_key: str = "LOG_CFG",
        force: bool = True,
    ):
        """Setup logging configuration.

        :param default_path: Default path to logging config file.
        :param default_level: Default log-level (Logging.INFO).
        :param env_key: Environment key to use for logging configuration.
        :param force: Force logging configuration.
        """
        if not cls.initialized or force:
            path = default_path
            if value := os.getenv(env_key, None):
                path = value
            if os.path.exists(path):
                with open(path) as f:
                    config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            else:
                logging.basicConfig(level=default_level)
                logging.basicConfig(
                    level=default_level,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    filename="dfpy_s3utils.log",
                    filemode="w",
                )
            logging.getLogger("dfpy_s3utils").setLevel(default_level)
            cls.initialized = True


def attach_log(
    obj,
    log_level: int = logging.INFO,
    default_level: int = None,
    default_path: str = "logging.yaml",
    env_key: str = "LOG_CFG",
):
    """Function decorator to attach Logger to functions.

    :param obj: Logger function or class to attach the logging to.
    :param log_level: log-level for the current object logging.
    :param default_path: Default path to logging config file.
    :param default_level: Default log-level (Logging.INFO).
    :param env_key: Environment key to use for logging configuration.

    :returns: Object with attached logging instance
    """
    if callable(obj):
        __logger = logging.getLogger(obj.__qualname__.rsplit(".", 1)[0])
        if __logger.level == logging.DEBUG:

            @wraps(obj)
            def wrapper(*args, **kwargs):
                call_signature = ", ".join([repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()])
                __logger.debug(f"function {obj.__name__} called with args {call_signature}")
                try:
                    return obj(*args, **kwargs)
                except Exception as e:
                    __logger.exception(f"Exception raised in {obj.__name__}. exception: {str(e)}")
                    raise e

            return wrapper
        return obj
    obj.logger = logging.getLogger(obj.__class__.__name__)
    obj.logger.setLevel(log_level)
    if default_level:
        DefaultLogger.setup_logging(default_path, default_level, env_key, force=False)


class LoggerMetaClass(type):
    """LoggerMetaClass used by LoggerInterface."""

    def __new__(mcs, classname, bases, class_dict):  # noqa: N804
        """Function to create new Logger."""
        new_class_dict = {}
        for attribute_name, attribute in class_dict.items():
            if isinstance(attribute, FunctionType):
                # replace it with a wrapped version
                attribute = attach_log(attribute)
            new_class_dict[attribute_name] = attribute
        return type.__new__(mcs, classname, bases, new_class_dict)


class LoggerInterface(metaclass=LoggerMetaClass):
    """LoggerInterface to instantiate from."""

    logger = logging.getLogger()

    def __init__(
        self,
        log_level=logging.INFO,
        default_path="logging.yaml",
        default_level=logging.INFO,
        env_key="LOG_CFG",
        **kwargs,
    ):
        """Function decorator to attach Logger to functions.

        :param log_level: log-level for the current object logging.
        :param default_path: Default path to logging config file.
        :param default_level: Default log-level (Logging.INFO).
        :param env_key: Environment key to use for logging configuration.
        :param kwargs: Passed other parameters.

        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)
        DefaultLogger.setup_logging(default_path, default_level, env_key, force=False)
        super().__init__(**kwargs)
