#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""."""

import functools
from pyrigate.user_settings import settings


def configurable(setting):
    """Return a function that only gets called if a setting is enabled."""
    def decorator(func):
        @functools.wraps(func)
        def _configurable(*args, **kwargs):
            if settings[setting]:
                return func(*args, **kwargs)

        return _configurable

    return decorator
