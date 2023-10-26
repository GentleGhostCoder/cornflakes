import logging

from cornflakes.decorator.click.options._global import global_option
from cornflakes.logging.logger import setup_logging


@global_option(
    ["-v", "--verbose"],
    help="Set logging level is set to logging.DEBUG for module-level loggers.",
    is_flag=True,
)
@global_option(
    ["-vv", "--verbose-all"],
    help="Set logging level is set to logging.DEBUG for all loggers.",
    is_flag=True,
)
@global_option(
    ["--log-config"],
    help="Change The default logging configuration file path (current only yaml format supported).",
    type=str,
    default="logging.yaml",
)
def verbose_option(verbose, verbose_all, log_config, self):
    """Default Option for verbose logging.

    Example logging.yaml:

    .. code-block:: yaml

        version: 1
        disable_existing_loggers: False
        formatters:
          simple:
            format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
          ecs_formatter:
            (): ecs_logging.StdlibFormatter

        handlers:
          console:
            class: logging.StreamHandler
            level: INFO
            formatter: simple
            stream: ext://sys.stdout

          info_file_handler:
            class: logging.handlers.RotatingFileHandler
            level: INFO
            formatter: simple
            filename: info.log
            maxBytes: 10485760 # 10MB
            backupCount: 20
            encoding: utf8

          error_file_handler:
            class: logging.handlers.RotatingFileHandler
            level: ERROR
            formatter: simple
            filename: errors.log
            maxBytes: 10485760 # 10MB
            backupCount: 20
            encoding: utf8

        loggers:
          <logger-name>:
            level: DEBUG
            handlers: [ console ]
            propagate: no

        root:
          level: DEBUG
          handlers: [console]


    Default logging.yaml:

    .. code-block:: yaml

        version: 1
        disable_existing_loggers: False
        formatters:
          default:
            format: '[%(name)s] - %(funcName)s() - %(message)s'
            datefmt: '[%Y-%m-%d %H:%M:%S.%f]'
        handlers:
          default:
            class: rich.logging.RichHandler
            level: !py "default_level or logging.root.level"
            formatter: default
        root:
          level: !py "default_level or logging.root.level"
          handlers:
            - default

    """
    if verbose_all:
        setup_logging(default_level=logging.DEBUG, force=True)
        return

    loggers = []
    if self.callback.__module__:
        main_module_name = self.callback.__module__.split(".", 1)[0] if self.callback.__module__ else None
        loggers = [logger for logger in logging.root.manager.loggerDict if main_module_name in logger]
    if hasattr(self, "config") and hasattr(self.config, "VERBOSE_LOGGER") and len(self.config.VERBOSE_LOGGER):
        loggers.extend(self.config.VERBOSE_LOGGER)
    setup_logging(
        default_level=logging.DEBUG if verbose else logging.root.level, loggers=loggers, default_path=log_config
    )
