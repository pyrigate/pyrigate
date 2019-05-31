# -*- coding: utf-8 -*-

"""Logging and output functions."""

import datetime
import logging
import os
from pathlib import Path
from pyrigate.config import configurable
from pyrigate.settings import settings


@configurable('logging')
def setup_logging(settings):
    """Setup logging."""
    log_dir = Path(settings['log_dir'])

    try:
        os.mkdir(log_dir)
    except OSError:
        error("Failed to create directory '{0}' for logging"
              .format(log_dir))

    log_format = settings['log_format']
    log_file = '{0}_pyrigate.log'.format(datetime.now())
    log_file_path = log_dir / log_file

    logging.basicConfig(filename=log_file_path,
                        format=log_format,
                        level=logging.INFO)


def _internal_log(log_func, exception, msg, *args, **kwargs):
    """Internal, multi-purpose logging function."""
    if kwargs.get('verbosity', 1) > settings['verbosity'] and not exception:
        return

    fmsg = "{0} {1}{2}".format(settings['prefix'], msg, settings['suffix'])

    if settings['logging']:
        log_func(msg, *args, **kwargs)

    print(fmsg.format(*args, **kwargs))

    if exception:
        raise exception(msg.format(*args, **kwargs))


def output(msg, *args, **kwargs):
    """Output a message to the console without any logging."""
    print(msg.format(*args, **kwargs))


def log(msg, *args, **kwargs):
    """Log a message."""
    _internal_log(logging.info, None, msg, *args, **kwargs)


def error(exception, msg, *args, **kwargs):
    """Log a message then raise an exception."""
    _internal_log(logging.error, exception, msg, *args, **kwargs)
