#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Base class for all jobs."""

import threading


class Job:
    """A periodic job."""

    _FREQUENCIES = ('daily', 'weekly', 'monthly', 'yearly')

    def __init__(self, frequency):
        if not self.is_valid_frequency(frequency):
            raise ValueError("Invalid frequency '{0}'".format(frequency))

        self._frequency = frequency
        self._event = threading.Event()

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

    def do(self):
        """Execute the job."""
        raise NotImplementedError()
