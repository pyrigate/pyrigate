#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""."""

import threading


class Job(object):

    """A pyrigate watering job."""

    def __init__(self):
        self._event = threading.Event()

    @classmethod
    def from_string(cls, s):
        """."""
        pass
