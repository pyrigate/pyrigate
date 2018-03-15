#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""pyrigate settings."""


settings = {
    # Prefix used for pyrigate console output
    'prefix': '💦 🌱 ',

    # Degree of status output, higher means more and 0 silences all output
    'verbosity': 1,

    # Whether or not to log system status
    'logging': False,

    # Logging format. Default displays as:
    # '[2006-02-08 22:20:02] INFO: Error message (pyrigate.function)'
    'log_format': '[%(asctime)s] %(levelname)s: %(message)s '
                  '(%(module)s.%(funcName)s)',

    # Logging directory
    'log_dir': './logs',

    # Send a warning when water levels are below this level (in deciliter)
    'warn_at_water_level': 0.1,

    # If True, sends status updates each week to the addresses listed in
    # email.subscribers
    'status_updates': True,

    # Email subconfiguration
    'email': {
        # Send a warning email about low water levels to these emails
        'subscribers': [],

        # SMTP server to use
        'server': 'localhost',

        # Port through which to connect to the server
        'port': 25,

        # Use SSL encryption when sending emails
        'use_ssl': True
    },

    # A list of all connected pumps. Requires at least a specified connecting
    # GPIO pin and a flow rate
    'pumps': {
        'main': {
            'pin': 7,
            'flow_rate': '1.2L/min'
        }
    }
}
