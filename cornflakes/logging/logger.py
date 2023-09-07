from functools import wraps
from inspect import isclass
import logging
import logging.config
import os
from types import FunctionType
from typing import Any, Callable, List, Optional, Protocol, Union

import yaml


def setup_logging(  # noqa: C901
    default_path: str = "logging.yaml",
    default_level: Optional[int] = None,
    env_key: str = "LOG_CFG",
    force: bool = False,
    loggers: Optional[List[str]] = None,
    handlers: Optional[List[str]] = None,
    **kwargs,
):
    """Setup logging configuration.

    :param force: Overwrite current log-level
    :param default_path: Default path to logging config file.
    :param default_level: Default log-level (Logging.INFO).
    :param env_key: Environment key to use for logging configuration.
    :param loggers: List of loggers to set log-level for.
    :param handlers: List of handlers to set log-level for.
    :param kwargs: arguments to pass to rich_handler
    """
    if value := os.getenv(env_key, None):
        default_path = value

    if os.path.exists(default_path):
        with open(default_path) as f:
            config = yaml.safe_load(f.read())
            if default_level:
                if force:
                    for handler_name in config["root"]["handlers"]:
                        if handlers and handler_name in handlers:
                            config["handlers"][handler_name]["level"] = default_level or logging.root.level
                    for logger in config["root"]["loggers"]:
                        if loggers and logger in loggers:
                            config["loggers"][logger]["level"] = default_level or logging.root.level
                config["root"]["level"] = default_level or logging.root.level
            logging.config.dictConfig(config)
    else:
        logging.config.dictConfig(
            {
                "version": 1,
                "formatters": {
                    "default": {
                        "format": "[%(name)s] - %(funcName)s() - %(message)s",
                        "datefmt": "[%Y-%m-%d %H:%M:%S.%f]",
                    },
                },
                "handlers": {
                    "default": {
                        "class": "rich.logging.RichHandler",
                        "level": default_level or logging.root.level,
                        "formatter": "default",
                    },
                },
                "root": {
                    "level": default_level or logging.root.level,
                    "handlers": ["default"],
                },
                "disable_existing_loggers": not force,
            }
        )
        for handler in logging.root.handlers:
            if hasattr(handler, "setLevel") and force:
                handler.setLevel(default_level or logging.root.level)
        for logger_name, logger in logging.root.manager.loggerDict.items():
            if isinstance(logger, logging.Logger) and loggers and logger_name in loggers:
                logger.disabled = False
                logger.setLevel(default_level or logging.root.level)
        if isinstance(logging.root, logging.Logger):
            logging.root.setLevel(default_level or logging.root.level)


class LoggerMetaClass(type):
    """LoggerMetaClass used for  metaclass."""

    def __new__(cls, classname, bases, class_dict):  # noqa: N804
        """Method __new__ for LoggerMetaClass."""
        new_class_dict = {}
        for attribute_name, attribute in class_dict.items():
            if isinstance(attribute, FunctionType):
                # replace it with a wrapped version
                attribute = attach_log(attribute)
            new_class_dict[attribute_name] = attribute
        cls.logger = logging.getLogger(classname)
        return type.__new__(cls, classname, bases, new_class_dict)


class LoggerProtocol(Protocol):
    """LoggerProtocol used for Type Annotation."""

    logger: logging.Logger


def __wrap_class(
    w_obj,
    log_level: Optional[int] = None,
):
    w_obj.logger = logging.getLogger(f"{w_obj.__module__}.{w_obj.__name__}")
    w_obj.logger.setLevel(log_level or logging.root.level)

    if w_obj.logger.level == logging.DEBUG:
        for attribute_name, attribute in w_obj.__dict__.items():
            if isinstance(attribute, FunctionType):
                # replace it with a wrapped version
                attribute = attach_log(
                    obj=attribute,
                    log_level=log_level,
                )
                setattr(w_obj, attribute_name, attribute)
    return w_obj


def __wrap_function(
    w_obj,
    log_level: Optional[int] = None,
):
    logger = logging.getLogger(f"{w_obj.__module__}.{w_obj.__qualname__}")
    logger.setLevel(log_level or logging.root.level)
    if logger.level != logging.DEBUG:
        return w_obj

    @wraps(w_obj)
    def wrapper(*args, **kwargs):
        call_signature = ", ".join([repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()])
        logger.debug(f"function {w_obj.__name__} called with args {call_signature}")
        try:
            return w_obj(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Exception raised in {w_obj.__name__}. exception: {str(e)}")
            raise e

    return wrapper


def attach_log(
    obj=None,
    log_level: Optional[int] = None,
    default_level: Optional[int] = None,
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
    if default_level:
        setup_logging(default_path, default_level, env_key, force=True)

    def obj_wrapper(w_obj) -> Union[LoggerProtocol, Callable[..., Any]]:
        if isclass(w_obj):
            return __wrap_class(w_obj, log_level)

        return __wrap_function(w_obj, log_level) if callable(w_obj) else obj

    return obj_wrapper(obj) if obj else obj_wrapper
