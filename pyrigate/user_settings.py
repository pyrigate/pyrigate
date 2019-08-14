#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""pyrigate user settings."""

import schema
import sys

from pyrigate.validation import settings_schema


values = {
    # Prefix used for pyrigate console output
    'prefix': '💦 🌱 ',

    # Degree of status output, higher means more and 0 silences all output
    'verbosity': 1,

    # Whether or not to log system status
    'logging': True,

    # Logging format. Default displays as:
    # '[2006-02-08 22:20:02] INFO: This is the error message'
    'log_format': '[{asctime}] {levelname}: {message} ',

    # Logging directory relative to the parent of pyrigate's top-level package
    'log_dir': './logs',

    # Send a warning when water levels are below this level (in deciliter)
    'warn_at_water_level': 0.1,

    # If True, send status updates to the addresses listed in email.subscribers
    # as dictated by 'status_frequency'
    'status_updates': False,

    # Send status updates with this frequency
    'status_frequency': 'weekly',

    # Email subconfiguration
    'email': {
        # The mail to send notifications from
        'sender': 'pyrigate@gmail.com',

        # Send a warning email about low water tank levels to these emails
        'subscribers': ['albo.developer@gmail.com'],

        # SMTP server to use
        'server': 'smtp.gmail.com',

        # Port through which to connect to the server
        'port': 587,

        # Use SSL encryption when sending emails
        'use_ssl': False
    },

    # A list of all connected pumps. Requires at least specifying the gpio pin
    # and flow rate
    'pumps': {
        'main': {
            'pin': 7,
            'flow_rate': '1.2L/min'
        }
    }
}


##########################################################
# !!! USERS SHOULD NOT MODIFY ANYTHING BELOW THIS LINE !!!
##########################################################
try:
    settings = settings_schema.validate(values)
except schema.SchemaError as ex:
    errors = [e for e in ex.autos + ex.errors if e]
    print('Failed to load settings: {0}'.format(' '.join(errors)))
    sys.exit(1)
