#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""."""

from pyrigate.jobs import Job
from pyrigate.log import warn
import threading


class StatusReportJob(Job):
    """A pyrigate job for sending periodic status reports."""

    def __init__(self, settings):
        super().__init__()

        self._should_update = settings['status_updates']
        self._frequency = settings['status_frequency']

    def schedule(self, scheme, job):
        """."""
        if self.frequency == 'daily':
            schedule.every().day.do(self.do)
        elif self.frequency == 'weekly':
            schedule.every().week.do(self.do)
        elif self.frequency == 'monthly':
            schedule.every(interval=4).weeks.do(self.do)
        elif self.frequency == 'yearly':
            schedule.every(interval=52).weeks.do(self.do)

    def do(self, email):
        email_settings = settings['email']

        send_mail(
            'Pyrigate {} status report'.format(self.frequency),
            email_settings['sender'],
            email_settings['subscribers'],
            'TODO',
            email_settings['server'],
            email_settings['port']
        )
