# -*- coding: utf-8 -*-

"""Base class for all sensors."""

from abc import ABCMeta, abstractmethod
import pyrigate.gpio as gpio


class Sensor(object, metaclass=ABCMeta):
    """Base class for all sensors."""

    def __init__(self, pin, threshold, analog):
        """Initialise the sensor with an input pin and a trigger threshold."""
        self._pin = pin
        self._threshold = threshold
        self._analog = analog

        gpio.setup(pin, gpio.INPUT)

    @property
    def pin(self):
        """Return the pin number for the sensor's gpio connector."""
        return self._pin

    @property
    def threshold(self):
        """Return the threshold at which this sensor is triggered."""
        return self._threshold

    @property
    @abstractmethod
    def triggered(self):
        """Return True if the sensor was triggered."""
        pass

    @property
    def analog(self):
        """Return True if the sensor is analog, False if it is digital."""
        return self._analog

    def read(self):
        """Read a analog/digital value from the sensor."""
        return gpio.input(self.pin)
