# -*- coding: utf-8 -*-

"""Base class for all sensors."""

from abc import ABCMeta, abstractmethod


class Sensor(object):
    """Base class for all sensors."""

    __metaclass__ = ABCMeta

    def __init__(self, pin, threshold, analog):
        """"""
        self._pin = pin
        self._threshold = threshold
        self._analog = analog

    @property
    def pin(self):
        """Return the pin number for the sensor's GPIO connector."""
        return self._pin

    @property
    def threshold(self):
        """Return the threshold at which this sensor is triggered."""
        return self._threshold

    @property
    @abstractmethod
    def triggered(self):
        """Return True if the sensor was triggered."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def analog(self):
        """Return True if the sensor is analog, False if it is digital."""
        return self._analog

    @abstractmethod
    def read(self):
        """Read a analog/digital value from the sensor."""
        raise NotImplementedError()
