#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""."""

import schedule
from pyrigate.jobs import Job
from pyrigate.units.parse import parse_unit


class WateringJob(Job):
    """A pyrigate watering job."""

    def __init__(self, controller, config=None):
        super().__init__()
        self._description = ''
        self._controller = controller

        if config:
            self.schedule(config)

    def schedule(self, config):
        """Schedule a watering job from a plant configuration."""
        self._config = config
        scheme = config.scheme
        amount = scheme['amount']

        for when in scheme['when']:
            job = None

            if 'on' in when:
                job = self._schedule_on_type(when['on'])
            else:
                job = self._schedule_each_type(when['each'])

            for time in when['at']:
                job = getattr(job, 'at')(time)

            job.do(self.task, amount)

    def _schedule_on_type(self, on):
        return getattr(schedule.every(), on)

    def _schedule_each_type(self, each):
        if each == 'month':
            return schedule.every(interval=4).weeks
        elif each == 'year':
            return schedule.every(interval=52).weeks
        else:
            return getattr(schedule.every(), each)

    def task(self, amount_string):
        pump = self._controller.get_pump(self._config.scheme['pump'])

        if pump:
            self._runs += 1
            pump.pump_unit(*parse_unit(amount_string))

    @property
    def description(self):
        return self._config.schedule_description

    @property
    def type(self):
        return self._type
