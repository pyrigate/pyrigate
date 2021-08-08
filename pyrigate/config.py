#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generic plant configuration class."""

import json
import os

from pyrigate.validation import plant_configuration_schema


class ConfigError(Exception):
    pass


class PlantConfiguration:

    """Light-weight configuration class for plants.

    Its main purpose is to provide sensible defaults when certain setting are
    not found.

    """

    def __init__(self, path=None):
        """Initialise a configuration, optionally reading from a file."""
        self._path = path
        self._schedule_description = ''
        self._config = {}
        self.load(path)

    @classmethod
    def extension(cls):
        """File extension of configuration files."""
        return 'json'

    def load(self, path):
        """Load a plant configuration from a file."""
        if path:
            self._path = path

            with open(path) as fh:
                self._config =\
                    plant_configuration_schema.validate(json.load(fh))

                self._schedule_description =\
                    self._create_description(self._config)

                return True

        return False

    def _create_description(self, config):
        """Create a human-readable description of the config's schedule."""
        descriptions = []

        for when in config['scheme']['when']:
            description = []

            if 'on' in when:
                description.append(f"on {when['on']}s at")
            else:
                description.append(f"each {when['each']} at")

            for time in when['at']:
                description.append(time)

            descriptions.append(' '.join(description))

        return ' and '.join(descriptions)

    @property
    def valid(self):
        return bool(self._config)

    @property
    def path(self):
        return self._path

    @property
    def description(self):
        return self._config['description']

    @property
    def name(self):
        return self._config['name']

    @property
    def schedule_description(self):
        return self._schedule_description

    @property
    def scheme(self):
        return self._config['scheme']

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value
