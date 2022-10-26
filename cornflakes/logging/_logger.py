from functools import wraps
from inspect import isclass
import logging
import logging.config
import os
import sys
from types import FunctionType
from typing import Any, Callable, Optional, Union

import yaml


def default_logger_decorator(cls):
    """Decorator for logging.Logger to redefine Logger.name at each log."""

    def log_func_decorator(func):
        def wrapper(*args, **kwargs):
            cls.name = sys._getframe(2).f_code.co_name
            return func(*args, **kwargs)

        return wrapper

    cls._log = log_func_decorator(cls._log)

    return cls


logger = default_logger_decorator(logging.getLogger("default-logger"))

logger.initialized = False
logger.default_level = logging.DEBUG


def setup_logging(
    default_path: str = "logging.yaml",
    default_level: Optional[int] = None,
    env_key: str = "LOG_CFG",
    force: bool = True,
):
    """Setup logging configuration.

    :param default_path: Default path to logging config file.
    :param default_level: Default log-level (Logging.INFO).
    :param env_key: Environment key to use for logging configuration.
    :param force: Force logging configuration.
    """
    if not logger.initialized or force:
        path = default_path
        if value := os.getenv(env_key, None):
            path = value

        if default_level:
            default_level = default_level

        if os.path.exists(path):
            with open(path) as f:
                config = yaml.safe_load(f.read())
            if default_level:
                for handler in config["root"]["handlers"]:
                    config["handlers"][handler]["level"] = default_level
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(
                level=default_level,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                filename="default.log",
                filemode="w",
            )
        logging.getLogger().setLevel(default_level)
        logger.initialized = True


logger.setup_logging = setup_logging


class LoggerMetaClass(type):
    """LoggerMetaClass used for Type Annotation."""

    logger: logging.Logger = None


def attach_log(
    obj,
    log_level: int = logger.default_level,
    default_level: int = None,
    default_path: str = "logging.yaml",
    env_key: str = "LOG_CFG",
) -> Union[Callable[..., Any], LoggerMetaClass]:
    """Function decorator to attach Logger to functions.

    :param obj: Logger function or class to attach the logging to.
    :param log_level: log-level for the current object logging.
    :param default_path: Default path to logging config file.
    :param default_level: Default log-level (Logging.INFO).
    :param env_key: Environment key to use for logging configuration.

    :returns: Object with attached logging instance
    """
    if isclass(obj):
        obj.logger = logging.getLogger(obj.__class__.__name__)
        obj.logger.setLevel(log_level)
        if default_level:
            setup_logging(default_path, default_level, env_key, force=True)

        new_class_dict = {}
        for attribute_name, attribute in obj.__dict__.items():
            if isinstance(attribute, FunctionType):
                # replace it with a wrapped version
                attribute = attach_log(obj=attribute)
            new_class_dict[attribute_name] = attribute

        return obj.__name__(obj, obj.__name__, obj.__bases__, new_class_dict)

    if callable(obj):
        __logger = logging.getLogger(obj.__qualname__.rsplit(".", 1)[0])

        if __logger.level != logging.DEBUG:
            return obj

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
