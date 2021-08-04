#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A job to periodically a status report to stdout."""

from pyrigate.jobs import Job
from pyrigate.log import log
from pyrigate.user_settings import settings
import sys


class StatusReportStdoutJob(Job):
    """A pyrigate job for sending periodic status reports to stdout."""

    def __init__(self, frequency):
        super().__init__(frequency)

    def task(self):
        log('Sending status report to stdout')

        sys.stdout.write("""Pyrigate {0} status report:

        TODO

        """.format(self.frequency))
