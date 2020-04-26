#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Settings class for users."""

import importlib

import pyrigate
from pyrigate.pump import Pump
from pyrigate.default_settings import default_settings
# from pyrigate.logging import error
from pyrigate.user_settings import user_settings


class Settings:
    """Light-weight settings class for general pyrigate settings.

    Allows for dot access to settings:
    >>> settings.email.subscribers
    'me@mail.org'

    If the nested attributes are not available, a default or None is returned.
    """

    # Minimum required parameters for specific settings
    _REQUIRED_PARAMS = {
        'pumps': frozenset([
            'pin',
            'flow_rate'
        ]),
        'email': frozenset([
            'sender',
            'subscribers',
            'server'
        ])
    }

    def __init__(self):
        super().__init__()
        self.load(user_settings, default_settings)

    @property
    def deprecated(self):
        """Parameters that have been marked as deprecated."""
        return {}

    @property
    def future(self):
        """Parameters that will be available in the future."""
        return {
            'warn_at_water_level',
            'status_frequency'
        }

    @property
    def handlers(self):
        return {
            'pumps': self.set_pumps,
            'email': self.set_email
        }

    def _set_mapping(self, name, mapping):
        """Autogenerate a property."""
        self._settings[name] = mapping

    def is_required(self, param):
        """Return True if the parameter is required."""
        pass

    def set_pumps(self, pumps):
        """Handler for pump settings."""
        _pumps = {}

        for pump_name in pumps:
            _pumps[pump_name] = Pump(pump_name,
                                     pumps[pump_name]['pin'],
                                     pumps[pump_name]['flow_rate'])

        self._set_mapping('pumps', _pumps)

    def set_email(self, email):
        """Handler for email settings."""
        # for setting in ('sender', 'server'):
        #     if setting not in email:
        #         error(AttributeError,
        #               "Missing '{0}' in email "
        #               "configuration".format(setting))

        # if not email.get('subscribers', None):
        #     error(AttributeError,
        #           "Missing or empty 'subscribers' in email "
        #           "configuration")

        _email = {}

        for key in email:
            _email[key] = email.get(key, default_settings['email'][key])

        self._set_mapping('email', _email)

    def load(self, settings, default_settings):
        """Load user settings from pyrigate.user_settings.py."""
        self._settings = {}

        for setting in default_settings:
            # if setting in self.deprecated:
            #     pyrigate.output("Setting '{0}' is deprecated", setting)

            # if setting in self.future:
            #     pyrigate.output("Setting '{0}' will become available in the "
            #                     "future", setting)

            if setting in self.handlers:
                self.handlers[setting](settings[setting])
            else:
                self._settings[setting] =\
                    settings.get(setting, default_settings[setting])

    def reload(self):
        """Reload settings."""
        importlib.reload(pyrigate.user_settings)
        self.load(user_settings, default_settings)

    def list(self):
        """Print all current settings to the console."""
        for k, v in self._settings.items():
            print("{0}: {1}".format(k, v))

    def __getitem__(self, key):
        return self._settings.get(key, None)

    def __setitem__(self, key, value):
        self._settings[key] = value


_settings = Settings()


def get_settings():
    """Get global pyrigate settings."""
    return _settings
