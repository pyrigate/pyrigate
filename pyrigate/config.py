#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generic plant configuration class."""

import functools
import json
from pyrigate.logging import error


def configurable(config, setting):
    """Return a function that only gets called if a setting is enabled."""
    def decorator(func):
        @functools.wraps(func)
        def _configurable(*args, **kwargs):
            if config[setting]:
                return func(*args, **kwargs)

        return _configurable

    return decorator


class Configuration(object):
    """Light-weight configuration class for a specific plant.

    Its main purpose is to provide sensible defaults when certain setting are
    not found.

    """

    def __init__(self, filename=''):
        """Initialise a configuration, optionally reading from a file."""
        self._mapping = {}

        if filename:
            self.load(filename)

    @classmethod
    def required(cls):
        """Set of required configuration keys."""
        return frozenset([
            'name',
            'amount',
            'frequency',
            'per'
        ])

    @classmethod
    def extension(cls):
        """File extension of configuration files."""
        return 'json'

    def load(self, filename):
        """Load a configuration file."""
        with open(filename) as fh:
            self._config = json.load(fh)

            for key in Configuration.required():
                if key not in self._config:
                    error(AttributeError,
                          "'{0}' does not have required configuration key "
                          "'{1}'", filename, key)

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value

    def list(self):
        for k, v in self._config.items():
            print("{0:<20} {1:>20}".format(k, v))
