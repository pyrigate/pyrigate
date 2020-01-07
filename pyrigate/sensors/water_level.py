# -*- coding: utf-8 -*-

"""Water-level sensor controller class."""

from .sensors.sensor import Sensor


class WaterLevelSensor(Sensor):
    """Water-level sensor controller class."""

    def __init__(self, pin, threshold, analog):
        super().__init__(pin, threshold, analog)

    def read(self):
        return 0
