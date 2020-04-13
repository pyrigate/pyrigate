#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A job to periodically a status report to stdout."""

from pyrigate.jobs import Job
from pyrigate.log import log
from pyrigate.user_settings import settings
import sys
import schedule


class StatusReportStdoutJob(Job):
    """A pyrigate job for sending periodic status reports to stdout."""

    def __init__(self, frequency):
        super().__init__(frequency)

    def schedule(self, new_frequency=None):
        """Schedule this job, possibly with a new frequency."""
        if new_frequency and self.is_valid_frequency(new_frequency):
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
        log('Sending status report to stdout')

        sys.stdout.write("""Pyrigate {0} status report:

        TODO

        """.format(self.frequency))
