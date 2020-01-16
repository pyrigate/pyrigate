#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Logging and output functions."""

import colorise
import datetime
import logging
import os
from pathlib import Path
import sys

from pyrigate.decorators import configurable
from pyrigate.user_settings import settings


# Use new-style string formatting in logging calls. See the Python docs on the
# logging cookbook for details:
#
# https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook
class Message:
    def __init__(self, fmt, args):
        self.fmt = fmt
        self.args = args

    def __str__(self):
        return self.fmt.format(*self.args)

class NewStyleFormatAdapter(logging.LoggerAdapter):
    """Prefer using new-style string formatting for logging."""

    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            self.logger._log(level, Message(msg, args), (), **kwargs)


@configurable('logging')
def setup_logging():
    """Setup logging."""
    log_dir = Path(settings['log_dir'])

    try:
        os.mkdir(log_dir)
    except FileExistsError:
        pass
    except OSError:
        error("Failed to create directory '{0}' for logging"
              .format(log_dir))

    log_format = settings['log_format']
    now = datetime.datetime.now()
    log_file = '{0}_pyrigate.log'.format(now.strftime('%Y-%m-%d-%H-%M-%S'))
    log_file_path = log_dir / log_file

    # Set up the internal logging to use new-style formatting
    logging.basicConfig(filename=log_file_path,
                        format=log_format,
                        style='{',
                        level=logging.NOTSET)

    # Disable logging from the schedule library by allowing only critical
    # level messages (it currently emits only info level)
    logging.getLogger('schedule').setLevel(logging.CRITICAL)


# Create a logger object with our adapter to be used in this module
logger = NewStyleFormatAdapter(logging.getLogger())


def _internal_log(log_func, exception, msg, *args, **kwargs):
    """Internal, multi-purpose logging function."""
    verbosity = kwargs.pop('verbosity', settings['verbosity'])

    if verbosity > settings['verbosity'] and not exception:
        return

    should_raise = kwargs.pop('should_raise', False)
    fmsg = "{0}{1} {2}{3}".format(
        settings['prefix'],
        ' {{fg=red,bold}}Error:{{reset}}' if exception else '',
        msg,
        settings['suffix']
    )

    if settings['logging']:
        log_func(msg, *args, **kwargs)

    colorise.fprint(fmsg.format(*args, **kwargs), enabled=settings['colors'])

    if exception and should_raise:
        raise exception(msg.format(*args, **kwargs))


def output(msg, *args, **kwargs):
    """Output a message to the console without any logging."""
    colorise.fprint(msg.format(*args, **kwargs), enabled=settings['colors'])


def log(msg, *args, **kwargs):
    """Log a message."""
    _internal_log(logger.info, None, msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    """Warn the user about something."""
    msg = msg.format(*args, **kwargs)

    colorise.fprint('{{fg=yellow,bold}}WARNING:{{reset}} {0}'.format(msg),
                    file=sys.stderr, enabled=settings['colors'])


def error(exception, msg, *args, **kwargs):
    """Log a message then raise an exception."""
    _internal_log(logger.error, exception, msg, *args, **kwargs)
