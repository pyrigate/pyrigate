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


class NewStyleFormatLogRecord(logging.LogRecord):

    """Prefer using new-style string formatting."""

    def getMessage(self):
        msg = self.msg

        if self.args:
            if isinstance(self.args, dict):
                msg = msg.format(**self.args)
            else:
                msg = msg.format(*self.args)

        return msg


logging.setLogRecordFactory(NewStyleFormatLogRecord)


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

    logging.basicConfig(filename=log_file_path,
                        format=log_format,
                        level=logging.NOTSET)


def _internal_log(log_func, exception, msg, *args, **kwargs):
    """Internal, multi-purpose logging function."""
    verbosity = kwargs.pop('verbosity', settings['verbosity'])

    if verbosity > settings['verbosity'] and not exception:
        return

    should_raise = kwargs.pop('should_raise', False)
    fmsg = "{0}{1} {2}{3}".format(
        settings['prefix'],
        ' {{fg=red;bold}}Error:{{reset}}' if exception else '',
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
    _internal_log(logging.info, None, msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    """Warn the user about something."""
    colorise.fprint('{{fg=yellow,bold}}WARNING:{{reset}} {0}'
                    .format(*args, **kwargs), file=sys.stderr,
                    enabled=settings['colors'])


def error(exception, msg, *args, **kwargs):
    """Log a message then raise an exception."""
    _internal_log(logging.error, exception, msg, *args, **kwargs)
