#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""."""

from pyrigate.jobs import Job
from pyrigate.log import warn
import threading


class WateringJob(Job):
    """A pyrigate watering job."""

    def __init__(self, scheme=None):
        super().__init__()

        if scheme:
            self.schedule(scheme)

    def schedule(self, scheme, job):
        """."""
        if scheme['type'] == 'schedule':
            # Water plants at set intervals
            for wjob in scheme['when']:
                schedule = getattr(schedule.every(), scheme['day'])
                schedule = getattr(schedule, 'at')
                schedule = schedule(scheme['time'])
                schedule.do(job, scheme['amount'])
        elif scheme['type'] in ('auto',):
            # Water plants automatically based on a water humidity sensor
            warn("Scheme 'auto' not currently supported, job not scheduled")

    def do(self, amount):
        self.pump.pump(amount)

    @property
    def type(self):
        return self._type
