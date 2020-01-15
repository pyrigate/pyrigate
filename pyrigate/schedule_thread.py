#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Class for running scheduled jobs in the background."""

import schedule
import threading


# Adapted from run_continuously at
# https://github.com/mrhwick/schedule/blob/master/schedule/__init__.py
class ScheduleThread(threading.Thread):
    """Thread class for continuously running scheduled tasks."""

    def __init__(self, update_interval, *jobs):
        """Initialise with an update interval and a list of jobs.

        The update interval determines how often we check for scheduled jobs to
        run.

        """
        super().__init__()

        self._update_interval = update_interval
        self._jobs = jobs
        self._event = threading.Event()

    def run(self):
        """Run all scheduled jobs in the background."""
        while True:
            schedule.run_pending()

            if self._event.wait(timeout=self._update_interval):
                break

    def cancel(self):
        """Cancel all scheduled jobs."""
        self._event.set()

    @property
    def cancelled(self):
        """If all jobs have been cancelled or not."""
        return self._event.is_set()
