#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generic configuration class for watering and settings."""

import functools
import importlib
import pyrigate


def configurable(config, setting):
    """Return a function that only gets called if a setting is enabled."""
    def decorator(func):
        @functools.wraps(func)
        def _configurable(*args, **kwargs):
            if config[setting]:
                func(*args, **kwargs)

    return decorator


class Configuration(object):
    """Light-weight configuration class.

    Its main purpose is to provide sensible defaults when certain setting are
    not found.

    """

    _DEFAULT_CONFIG = {
        'name':      'unknown',
        'amount':    0,
        'frequency': 0,
        'per':       'unknown',
    }

    def __init__(self, filename=''):
        if filename:
            self.load(filename)

    def load(self, filename):
        """Load a configuration file."""
        config = importlib.import_module(filename)

        if not hasattr(config, 'configuration'):
            pyrigate.error(AttributeError, "'{0}' did not have any settings",
                           filename)

        if 'name' not in config.configuration:
            pyrigate.error(AttributeError,
                           "'{0}' does not have a required name", filename)

        self._set_values(config.configuration, Configuration._DEFAULT_CONFIG)

    def __getitem__(self, key):
        return self._mapping[key]

    def __setitem__(self, key, value):
        self._mapping[key] = value

    def _set_values(self, config, defaults):
        self._mapping = {}

        for attr in defaults:
            self._mapping[attr] = config.get(attr, defaults[attr])

    def list(self):
        print("{0:<20} {1:>20}".format('Name', self._mapping['name']))

        for k, v in self._mapping.items():
            if k != 'name':
                print("{0:<20} {1:>20}".format(k.title(), v))


class Settings(Configuration):
    """Light-weight settings class.

    Its main purpose is to provide sensible defaults when certain setting are
    not found.

    """

    def __init__(self):
        self.load()

    def load(self):
        """Load a settings file."""
        default_settings =\
            importlib.import_module('pyrigate.default_settings').settings
        settings = importlib.import_module('pyrigate.settings').settings

        self._set_values(settings, default_settings)
