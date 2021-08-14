#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Base class for all jobs."""

import schedule
import threading


class Job:
    """A periodic job."""

    def __init__(self):
        self._running = False
        self._runs = 0
        self._event = threading.Event()

    def schedule(self):
        """Schedule this job."""
        raise NotImplementedError()

    def stop(self):
        """Stop this job."""
        schedule.cancel_job(self)
        self._running = False

    @property
    def running(self):
        return self._running

    @property
    def runs(self):
        """How many times this job has run."""
        self._runs

    @property
    def tag(self):
        """The tag associated with this job."""
        raise NotImplementedError()

    def task(self):
        """Execute the job."""
        raise NotImplementedError()
