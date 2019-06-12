#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Core module for pyrigate."""

import os
import re
import schedule
import sys

import pyrigate
import pyrigate.gpio as gpio
from pyrigate.config import configurable, Configuration
from pyrigate.logging import setup_logging, error, log, output
from pyrigate.settings import get_settings

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
    regexes = [('hardware', re.compile(r'^Hardware\s+:\s+(.+)$')),
               ('revision', re.compile(r'^Revision\s+:\s+(.+)$'))]

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
    msg = 'pyrigate v{0}, Python {1}, Raspberry Pi '
    specs = rpi_specs()

    if gpio.mocked():
        msg += '(mocked)'
    else:
        msg += '{2} ({3})'.format(specs['version'], specs['model'])

    return msg.format(__version__,
                      '.'.join([str(v) for v in sys.version_info[:3]]))


def load_configs():
    """Load all configuration files found at the given path."""
    configs = []

    for dirpath, _, filenames in os.walk('configs'):
        for config in filenames:
            _, ext = os.path.splitext(config)

            if ext[1:] == Configuration.extension():
                configs.append(Configuration(os.path.join(dirpath, config)))

    return configs


# Global settings and plant configurations
settings = get_settings()
configs = load_configs()


def get_configs():
    return configs


def get_pump(name):
    """Get a pump by name."""
    return settings['pumps'][name]


def start():
    """Start pyrigate."""
    log('Starting pyrigate')

    if gpio.mocked():
        log('Not on a raspberry pi, gpio functions are being mocked')
    else:
        code = gpio.setup()

        if code != gpio.SETUP_OK:
            error('Failed to setup up gpio pins (code: {0})', code)

        gpio.setmode(gpio.BCM)

    setup_logging(settings)
    log('Loading plant configurations')

    pyrigate.load_configs()
    log('Loaded {0} plant configuration(s)', len(get_configs()),
        verbosity=2)

    for config in configs:
        log("Loaded config for '{0}'", config['name'])


@configurable(settings, 'status_updates')
def send_status_report():
    output('TODO: Send status report')


def schedule_tasks():
    """Schedule status reports, watering plans etc."""
    schedule.every().saturday.at('10:00').do(send_status_report)


def quit():
    """Quit pyrigate."""
    gpio.cleanup()
    log("Quitting pyrigate")


def run(args):
    """Runner function for pyrigate."""
    pyrigate.start()
    pyrigate.schedule_tasks()
    log('Running pyrigate')
    output("Type 'help' for information")
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
