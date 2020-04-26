#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Core module for pyrigate."""

import os
import re
import sys

import pyrigate.gpio as gpio

__version__ = '0.1.0'
__author__ = 'Alexander Asp Bock'
__license__ = 'MIT'


# Source:
# https://www.raspberrypi-spy.co.uk/2012/09/checking-your-raspberry-pi-board-version/
_REVISION_TO_MODEL = {
    '0002':   'Model B Rev 1',
    '0003':   'Model B Rev 1 ECN0001',
    '0004':   'Model B Rev 2',
    '0005':   'Model B Rev 2',
    '0006':   'Model B Rev 2',
    '0007':   'Model A',
    '0008':   'Model A',
    '0009':   'Model A',
    '000d':   'Model B Rev 2',
    '000e':   'Model B Rev 2',
    '000f':   'Model B Rev 2',
    '0010':   'Model B+',
    '0013':   'Model B+',
    '900032': 'Model B+',
    '0011':   'Compute Module',
    '0014':   'Compute Module',
    '0012':   'Model A+',
    '0015':   'Model A+',
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
        msg += '{0} ({1})'.format(specs['version'], specs['model'])

    return msg.format(__version__,
                      '.'.join([str(v) for v in sys.version_info[:3]]))
