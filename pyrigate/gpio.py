#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""GPIO control functions.

Mocks all functions (functions become no-ops) if we are not running on a
raspberry pi. See https://sourceforge.net/projects/raspberry-gpio-python/ for
details.

"""

from pyrigate.log import error, log

try:
    from RPi.GPIO import *

    def mocked():
        """Return True if gpio functions are being mocked."""
        return False
except ImportError:
    def mocked():
        """Return True if gpio functions are being mocked."""
        return True

    # Global variables
    SETUP_OK = 0
    SETUP_DEVMEM_FAIL = 1
    SETUP_MALLOC_FAIL = 2
    SETUP_MMAP_FAIL = 3
    SETUP_CPUINFO_FAIL = 4
    SETUP_NOT_RPI_FAIL = 5

    INPUT = 1
    OUTPUT = 0
    ALT0 = 4

    HIGH = 1
    LOW = 0

    PUD_OFF = 0
    PUD_DOWN = 1
    PUD_UP = 2

    def setup(*args, **kwargs):
        pass

    def cleanup(*args, **kwargs):
        pass

    def output(*args):
        pass

    def input(*args):
        pass

    def setmode(*args):
        pass

    def getmode(*args):
        pass

    def add_event_detect(*args, **kwargs):
        pass

    def remote_event_detect(*args):
        pass

    def event_detected(*args):
        return False

    def add_event_callback(*args, **kwargs):
        pass

    def wait_for_edge(*args, **kwargs):
        pass

    def gpio_function(*args):
        pass

    def setwarnings(*args):
        pass


def init():
    """Initialise gpio functionality."""
    if mocked():
        log('Not on a raspberry pi, mocking GPIO functionality')
    else:
        code = setup()

        if code != SETUP_OK:
            error('Failed to setup up GPIO pins (code: {0})', code)

        setmode(BCM)
        log('GPIO interface initialised', verbosity=2)
