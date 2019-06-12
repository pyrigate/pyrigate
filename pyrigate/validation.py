#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Validation schemas for settings and plant configurations."""

import re
from schema import Schema, Optional, Use, And, Regex


valid_status_frequencies = [
        'daily',
        'weekly',
        'monthly',
        'yearly'
    ]

valid_frequency = Use(str, lambda f: f in valid_status_frequencies)

# Recognises volume amount such as '1dl' or '0.1 cl'
valid_amount = Regex(r'^\d+(\.\d+)?\s*(ml|dl|cl|l)$', flags=re.IGNORECASE,
                     error='Not a valid amount')

# valid_flow_rate = Regex()


# Schema for validating user settings
settings_schema = Schema({
        Optional('prefix',              default='💦 🌱 '): str,
        Optional('suffix',              default=''):       str,
        Optional('verbosity',           default=1):        int,
        Optional('logging',             default=False):    bool,
        Optional('log_format',          default=''):       str,
        Optional('log_dir',             default='./logs'): str,
        Optional('warn_at_water_level', default=-1.0):     float,
        Optional('status_updates',      default=True):     bool,
        Optional('status_frequency',    default='weekly'): valid_frequency,
        Optional('email', default={}): {
                'sender':                          str,
                'subscribers':                     list,
                'server':                          str,
                'port':                            And(int, lambda p: p >= 0),
                Optional('use_ssl', default=True): bool,
            },
        Optional('pumps', default={}): {
                str: {
                    'pin':       And(int, lambda p: p >= 0),
                    'flow_rate': str
                }
            },
        Optional('sensors', default={}): {
                str: {
                    'pin': And(int, lambda p: p >= 0),
                    'threshold': str,
                    'trigger': str,
                    'analog': bool
                }
            }
    })

# Schema for validating json plant configurations
plant_configuration_schema = Schema({
        'name':      str,
        'scheme':    And(str, lambda s: s in ('auto', 'schedule')),
        'amount':    And(str, valid_amount),
        'frequency': int,
        'per':       str,
        'times':     list,
        Optional('description', default='N/A'): str,
        Optional('url', default='N/A'):         str
    })


if __name__ == "__main__":
    import json

    with open('configs/chili.json') as fh:
        config = json.load(fh)

    print(plant_configuration_schema.validate(config))
