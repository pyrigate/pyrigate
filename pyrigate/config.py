#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generic plant configuration class."""

import json
import os
from pyrigate.validation import plant_configuration_schema


class ConfigError(Exception):
    pass


class PlantConfiguration(object):

    """Light-weight configuration class for plants.

    Its main purpose is to provide sensible defaults when certain setting are
    not found.

    """

    def __init__(self, path=None):
        """Initialise a configuration, optionally reading from a file."""
        self._config = {}
        self.load(path)

    @classmethod
    def extension(cls):
        """File extension of configuration files."""
        return 'json'

    def load(self, path):
        """Load a plant configuration from a file."""
        if path:
            with open(path) as fh:
                self._config =\
                    plant_configuration_schema.validate(json.load(fh))

    @property
    def valid(self):
        return bool(self._config)

    @property
    def name(self):
        return self._config['name']

    @property
    def description(self):
        return self._config['description']

    @property
    def scheme(self):
        return self._config['scheme']

    @property
    def amount(self):
        return self._config['amount']

    @property
    def frequency(self):
        return self._config['frequency']

    @property
    def per(self):
        return self._config['per']

    @property
    def times(self):
        return self._config['times']

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value

    def __str__(self):
        result = []
        max_width = max(len(str(v)) for v in self._config.values())
        fmt = '{{bold}}{0:<20} {{reset}}{1:>{2}}'

        for k, v in self._config.items():
            line = fmt.format(k, str(v), max_width)
            result.append(line)

        return os.linesep.join(result)
