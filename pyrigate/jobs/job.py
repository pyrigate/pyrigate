#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Base class for all jobs."""

import schedule
import threading


class Job:
    """A periodic job."""

    def __init__(self):
        self._runs = 0
        self._event = threading.Event()

    def schedule(self):
        """Schedule this job."""
        raise NotImplementedError()

    @property
    def runs(self):
        """How many times this job has run."""
        self._runs

    @property
    def frequency(self):
        """The frequency with which this job is executed."""
        return self._frequency

    @classmethod
    def from_string(cls, s):
        """."""
        pass

    def is_valid_frequency(self, frequency):
        """Check if a frequency string is valid."""
        return frequency in self._FREQUENCIES

    def task(self):
        """Execute the job."""
        raise NotImplementedError()
