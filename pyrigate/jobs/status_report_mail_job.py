#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A job to periodically send a status report by mail."""

from pyrigate.jobs import Job
from pyrigate.log import log
from pyrigate.mail import send_mail
from pyrigate.user_settings import settings
import schedule


class StatusReportMailJob(Job):
    """A pyrigate job for sending periodic status reports by mail."""

    def __init__(self, frequency):
        super().__init__(frequency)

    def schedule(self, new_frequency=None):
        """Schedule this job, possibly with a new frequency."""
        if self.is_valid_frequency(new_frequency):
            self._frequency = new_frequency

        schedule.every(2).seconds.do(self.do)
        return

        if self.frequency == 'daily':
            schedule.every().day.do(self.do)
        elif self.frequency == 'weekly':
            schedule.every().week.do(self.do)
        elif self.frequency == 'monthly':
            schedule.every(interval=4).weeks.do(self.do)
        elif self.frequency == 'yearly':
            schedule.every(interval=52).weeks.do(self.do)

    def do(self):
        email_settings = settings['email']
        subscribers = email_settings['subscribers']
        log('Sending status report by mail {0}'.format(','.join(subscribers)))

        send_mail(
            'Pyrigate {} status report'.format(self.frequency),
            email_settings['sender'],
            subscribers,
            'TODO'
        )
