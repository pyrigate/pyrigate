#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Core module for pyrigate."""

import datetime
# import RPi.GPIO as gpio
import logging
import os
import pyrigate.config
from pyrigate.config import configurable
import pyrigate.mail
import re
import schedule
import sys

__version__ = '0.1.0'
__author__ = 'Alexander Asp Bock'
__license__ = 'MIT'


# Source:
# https://www.raspberrypi-spy.co.uk/2012/09/checking-your-raspberry-pi-board-version/
_REVISION_TO_MODEL = {
    '0002': 'Model B Rev 1',
    '0003': 'Model B Rev 1 ECN0001',
    '0004': 'Model B Rev 2',
    '0005': 'Model B Rev 2',
    '0006': 'Model B Rev 2',
    '0007': 'Model A',
    '0008': 'Model A',
    '0009': 'Model A',
    '000d': 'Model B Rev 2',
    '000e': 'Model B Rev 2',
    '000f': 'Model B Rev 2',
    '0010': 'Model B+',
    '0013': 'Model B+',
    '900032': 'Model B+',
    '0011': 'Compute Module',
    '0014': 'Compute Module',
    '0012': 'Model A+',
    '0015': 'Model A+',
    'a01041': 'Pi 2 Model B v1.1 (Sony, UK)',
    'a21041': 'Pi 2 Model B v1.1 (Embest, China)',
    'a22042': 'Pi 2 Model B v1.2 1GB',
    '900092': 'Pi Zero v1.2',
    '900093': 'Pi Zero v1.3',
    '9000C1': 'Pi Zero W',
    'a02082': 'Pi 3 Model B (Sony, UK)',
    'a22082': 'Pi 3 Model B (Embest, China)'
}


def rpi_specs():
    """Return the specifications of the running Raspberry Pi system.

    Currently attempts to find the hardware, version and model of the Raspberry
    Pi. Unknown or unavailable values are given as 'unknown'.

    """
    specs = {k: 'unknown' for k in ('hardware', 'version', 'model')}
    regexes = [('hardware', re.compile('^Hardware\s+:\s+(.+)$')),
               ('revision', re.compile('^Revision\s+:\s+(.+)$'))]

    if os.path.isfile('/proc/cpuinfo'):
        with open('/proc/cpuinfo', 'r') as fh:
            for line in fh:
                for key, regex in regexes:
                    m = regex.match(line)

                    if m:
                        specs[key] = m.group(1)

        try:
            ['BCM2708', 'BCM2709', 'BCM2835'].index(specs['hardware'])
        except IndexError:
            specs['number'] = 'unknown'

        if os.path.isfile('/proc/device-tree/model'):
            # This file should give us the full model name
            with open('/proc/device-tree/model') as fh:
                specs['model'] = fh.read()
        else:
            # Otherwise, attempt to get it from cpuinfo using a predefined
            # table of models
            if specs['revision'] != 'unknown':
                for revision in _REVISION_TO_MODEL:
                    if specs['revision'].lower() in revision:
                        specs['model'] = _REVISION_TO_MODEL[revision]
                        break

    return specs


def all_versions():
    """Return a string with the current pyrigate, Python and RPi versions."""
    specs = rpi_specs()

    return 'pyrigate v{0}, Python {1}, Raspberry Pi {2} ({3})'\
        .format(__version__, '.'.join([str(v) for v in sys.version_info[:3]]),
                specs['version'], specs['model'])


def load_settings():
    """Load and initialise pyrigate settings."""
    settings = pyrigate.config.Settings()
    settings['suffix'] = '...'

    return settings


def load_configs():
    """Load all configuration files found at the given path."""
    configs = []

    for item in os.listdir('pyrigate/configs'):
        if item == '__init__.py' or not item.endswith('.py'):
            continue

        name, ext = os.path.splitext(item)
        config = pyrigate.config.Configuration('pyrigate.configs.' + name)

        configs.append(config)

    return configs


# Global settings and plant configurations
settings = load_settings()
configs = load_configs()


@configurable(settings, 'logging')
def setup_logging(settings):
    """Setup logging."""
    print("Logging is enabled")
    try:
        os.mkdir(settings['log_dir'])
    except OSError:
        pass

    # Generate a new log file and set up logging
    log_file = '{0}_pyrigate.log'.format(datetime.datetime.now())
    log_file_full = os.path.join(settings['log_dir'], log_file)
    logging.basicConfig(filename=log_file_full,
                        format=settings['log_format'], level=logging.INFO)


def get_configs():
    return configs


def _internal_log(logger, exception, msg, *args, **kwargs):
    """Internal, multi-purpose logging function."""
    if kwargs.get('verbosity', 1) > settings['verbosity'] and not exception:
        return

    fmsg = "{0} {1}{2}".format(settings['prefix'], msg, settings['suffix'])

    if settings['logging']:
        logger(msg, *args, **kwargs)

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


def start():
    """Start pyrigate."""
    pyrigate.log('Starting pyrigate')
    # gpio.setmode(gpio.BCM)

    setup_logging(settings)

    pyrigate.log('Loading plant configurations')
    pyrigate.load_configs()
    pyrigate.log('Loaded {0} plant configuration(s)', len(get_configs()),
                 verbosity=2)

    for config in configs:
        pyrigate.log("Loaded config for '{0}'", config['name'])


@configurable(settings, 'status_updates')
def send_status_report():
    pyrigate.output('TODO: Send status report')


def schedule_tasks():
    """Schedule status reports, watering plans etc."""
    if pyrigate.settings['status_updates']:
        schedule.every().saturday.at('10:00').do(send_status_report)


def quit():
    """Quit pyrigate."""
    # gpio.cleanup()
    log("Quitting pyrigate")


def run(args):
    """Runner function for pyrigate."""
    pyrigate.start()
    pyrigate.schedule_tasks()
    pyrigate.log('Running pyrigate')
    interpreter = pyrigate.command.CommandInterpreter()

    try:
        while True:
            # TODO: Monitor plants, water them etc.
            interpreter.cmdloop()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        # Catch any other error, log it and reraise it
        pyrigate.error(None, e.message)
        raise
    finally:
        pyrigate.quit()
