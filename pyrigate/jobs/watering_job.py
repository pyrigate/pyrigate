#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""."""

import schedule
from pyrigate.jobs import Job


class WateringJob(Job):
    """A pyrigate watering job."""

    def __init__(self, config=None):
        super().__init__()
        self._description = ''

        if config:
            self.schedule(config)

    def schedule(self, config):
        """Schedule a watering job from a plant configuration."""
        descriptions = []
        scheme = config.scheme
        amount = scheme['amount']

        for when in scheme['when']:
            job = None
            description = []

            if 'on' in when:
                job = getattr(schedule.every(), when['on'])
                description.append('on ' + when['on'] + 's at')
            else:
                each = when['each']
                description.append('each ' + each + ' at')

                if each == 'month':
                    job = schedule.every(interval=4).weeks
                elif each == 'year':
                    job = schedule.every(interval=52).weeks
                else:
                    job = getattr(schedule.every(), when['each'])

            for time in when['at']:
                job = getattr(job, 'at')(time)
                description.append(time)

            job.do(self.task, amount)
            descriptions.append(' '.join(description))

        self._description = ' and '.join(descriptions)

    def task(self, amount):
        print('Watering {0}'.format(amount))
        self._runs += 1
        # self.pump.pump(amount)

    @property
    def description(self):
        return self._description

    @property
    def type(self):
        return self._type
