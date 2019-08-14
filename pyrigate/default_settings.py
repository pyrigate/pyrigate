#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""pyrigate default settings."""

#####################################################################
# !!! USERS SHOULD MODIFY 'user_settings.py' INSTEAD OF THIS FILE !!!
#####################################################################

defaults = {
    # Prefix used for pyrigate console output
    'prefix': '💦 🌱 ',

    # Degree of status output, higher means more and 0 silences all output
    'verbosity': 1,

    # Whether or not to log system status
    'logging': False,

    # Logging format. Default displays as:
    # '[2006-02-08 22:20:02] INFO: This is the error message'
    'log_format': '[{asctime}] {levelname}: {message} ',

    # Logging directory relative to the parent of pyrigate's top-level package
    'log_dir': './logs',

    # Send a warning when water levels are below this level
    'warn_at_water_level': '0.1dl',

    # If True, send status updates to the addresses listed in email.subscribers
    # as dictated by 'status_frequency'
    'status_updates': True,

    # Send status updates with this frequency
    'status_frequency': 'weekly',

    # Email subconfiguration
    'email': {
        # The mail to send notifications from
        'sender': '',

        # Send notifications to this list of subscribers
        'subscribers': [],

        # SMTP server to use
        'server': 'localhost',

        # Port through which to connect to the server
        'port': 25,

        # Use SSL encryption when sending emails
        'use_ssl': True
    },

    # A list of all connected pumps. Requires at least specifying the gpio
    # output pin and flow rate
    'pumps': {
        'main': {
            'pin': 7,
            'flow_rate': '1.2L/min'
        }
    },

    # A list of all connected sensors. Requires at least specifying the gpio
    # input pin and analog/digital. The threshold can be specified if the
    # sensor needs to trigger some action when it is crossed.
    #
    # Only moisture sensors and the 'water' action are currently supported.
    'sensors': {
        'moisture-sensor': {
            'pin': 5,
            'threshold': 0.1,
            'trigger': 'water',
            'analog': False
        }
    }
}
