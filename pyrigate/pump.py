# -*- coding: utf-8 -*-

"""Water pump controller class."""

import RPi.GPIO as gpio
import re
import time


_UNIT_CONVERSIONS = {
    'l': 1000.,
    'cl': 100.,
    'dl': 10.,
    'hour': 3600.,
    'min': 60.,
    'second': 1.
}


class WaterPump(object):
    """Water pump controller class."""

    @classmethod
    def convert_flowrate(cls, flow_rate, unit):
        """Convert a flow rate to a given unit."""
        volume_unit, time_unit = unit.split('/')

        try:
            return flow_rate * _UNIT_CONVERSIONS[volume_unit.lower()] /\
                _UNIT_CONVERSIONS[time_unit.lower()]
        except KeyError:
            raise ValueError("Unknown unit: '{0}'".format(unit))

    def __init__(self, pin, flow_rate, water_level_sensor=None):
        self._level = 0
        self.pin = pin
        self.flow_rate = flow_rate
        self.water_level_sensor = water_level_sensor
        gpio.setup(pin, gpio.OUT)

    @property
    def level(self):
        """Return current water level."""
        if self.water_level_sensor is None:
            # No sensor attached, cannot read the water level
            return -1
        else:
            # return self.water_level_sensor.read()
            return self._level

    @property
    def pin(self):
        """Return connecting GPIO pin."""
        return self._pin

    @pin.setter
    def pin(self, pin):
        """Set the GPIO pin for the pump."""
        self._pin = pin

    @property
    def flow_rate(self):
        """Return the pump's flow rate in milliter per second."""
        return self._flow_rate

    @flow_rate.setter
    def flow_rate(self, value):
        """Set pump flow rate."""
        if type(value) in (int, float):
            self._flow_rate = value
        else:
            m = re.match('(\d+(\.\d+)?)\s*([A-Za-z]+/[A-Za-z]+)', value)

            if m:
                self._flow_rate = WaterPump.convert_flowrate(float(m.group(1)),
                                                             m.group(3))
            else:
                raise ValueError("Unrecognised flow rate format: '{0}'"
                                 .format(value))

    def activate(self):
        """Activate the pump."""
        gpio.output(self.pin, False)

    def deactivate(self):
        """Deactivate the pump."""
        gpio.output(self.pin, True)

    def pump(self, amount):
        """Pump the given amount of water."""
        if self.level <= 0:
            return

        self.activate()
        time.sleep(amount / self.flow_rate)
        self.deactive()

        self._level -= amount

    def pump_timed(self, duration):
        """Pump water for a given amount of seconds."""
        if self.level <= 0:
            return

        self.activate()
        time.sleep(duration)
        self.deactive()

        # TODO: Use a water level sensor instead
        self._level -= duration * self.flow_rate

    def __repr__(self):
        return "{0}(pin={1}, flow_rate={2} mL/s)"\
            .format(self.__class__.__name__, self.pin, self.flow_rate)
