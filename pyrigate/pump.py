# -*- coding: utf-8 -*-

"""Water pump class."""

import RPi.GPIO as gpio
import time


class WaterPump(object):
    """Water pump controller class."""

    # Amount of water in ml pumped per millisecond
    ML_PER_MILLISECOND = 100

    def __init__(self, pin, diameter):
        self._level = 0
        self._pin = pin
        self._diameter = diameter
        gpio.setup(pin, gpio.OUT)

    @property
    def level(self):
        """Return current water level."""
        return self._level

    @property
    def pin(self):
        """Return connecting GPIO pin."""
        return self._pin

    @property
    def diameter(self):
        """Return pump wire diameter."""
        return self._diameter

    def activate(self):
        """Activate the pump."""
        gpio.output(self.pin, False)

    def deactivate(self):
        """Deactivate the pump."""
        gpio.output(self.pin, True)

    def pump(self, duration):
        """Pump water for some given seconds."""
        if self.level <= 0:
            return

        self.activate()
        time.sleep(duration)
        self.deactive()

        # TODO: Use a water level sensor instead
        self._level -= duration * self.ML_PER_MILLISECOND
