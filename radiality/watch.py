"""
radiality:radiality.watch

The `radiality/watch.py` is a part of `radiality`.
Apache 2.0 licensed.
"""

import os
import logging
import logging.config

from radiality import utils


class Logger:
    """
    Logging
    """
    _applog = None  # `logging`'s logger instance

    def __init__(self, config_path, name):
        """
        Setups the logging configuration
        """
        if os.path.exists(config_path):
            config = utils.load_config(config_path)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=logging.DEBUG)
            name = None

        self._applog = logging.getLogger(name)

    @property
    def applog(self):
        """
        Returns the current logger for the application
        """
        return self._applog


class Loggable:
    """
    Mixin for the capability of being recorded in a log
    """
    _logger = None  # type: Logger

    def log(self, msg, *args, **kwargs):
        """
        Logs the info message
        """
        if self._logger:
            self._logger.applog.info(msg, *args, **kwargs)
        else:
            print('INFO: ' + msg)

    def warn(self, msg, *args, **kwargs):
        """
        Logs the warning message
        """
        if self._logger:
            self._logger.applog.warning(msg, *args, **kwargs)
        else:
            print('WARN: ' + msg)

    def fail(self, msg, *args, **kwargs):
        """
        Logs the error message
        """
        if self._logger:
            self._logger.applog.error(msg, *args, **kwargs)
        else:
            print('FAIL: ' + msg)
