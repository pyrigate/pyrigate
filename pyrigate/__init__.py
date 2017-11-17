#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Core module for pyrigate."""

import datetime
# import RPi.GPIO as gpio
import logging
import os
import pyrigate.config
import pyrigate.mail
import schedule
import sys

__version__ = '0.1.0'
__author__ = 'Alexander Asp Bock'
__license__ = 'MIT'


def all_versions():
    return 'pyrigate v{0}, Python {1}, Raspberry Pi {2}'\
        .format(pyrigate.version(),
                '.'.join([str(v) for v in sys.version_info[:3]]),
                '?')


def load_settings():
    """Load and initialise pyrigate settings."""
    settings = pyrigate.config.Settings()

    if settings['logging']:
        try:
            os.mkdir(settings['log_dir'])
        except OSError:
            pass

        # Generate a new log file and set up logging
        log_file = '{0}_pyrigate.log'.format(datetime.datetime.now())
        log_file_full = os.path.join(settings['log_dir'], log_file)
        logging.basicConfig(filename=log_file_full,
                            format=settings['log_format'], level=logging.INFO)

    settings['suffix'] = '...'

    return settings


def load_configs():
    """Load all configuration files found at the given path."""
    configs = []

    for item in os.listdir('pyrigate/configs'):
        if item == '__init__.py' or item.endswith('.pyc'):
            continue

        name, ext = os.path.splitext(item)
        config = pyrigate.config.Configuration('pyrigate.configs.' + name)

        configs.append(config)

    return configs


# Global settings and plant configurations
settings = load_settings()
configs = load_configs()


def get_configs():
    return configs


def _internal_log(logger, exception, msg, *args, **kwargs):
    """Internal, multi-purpose logging function."""
    if kwargs.get('verbosity', 1) > settings['verbosity'] and not exception:
        return

    fmsg = "{0} {1}{2}".format(settings['prefix'], msg, settings['suffix'])

    if settings['logging']:
        logger(msg, *args, **kwargs)

    print(fmsg.format(*args, **kwargs))

    if exception:
        raise exception(msg.format(*args, **kwargs))


def output(msg, *args, **kwargs):
    """Output a message to the console without any logging."""
    print(msg.format(*args, **kwargs))


def log(msg, *args, **kwargs):
    """Log a message."""
    _internal_log(logging.info, None, msg, *args, **kwargs)


def error(exception, msg, *args, **kwargs):
    """Log a message then raise an exception."""
    _internal_log(logging.error, exception, msg, *args, **kwargs)


def start():
    """Start pyrigate."""
    pyrigate.log('Starting pyrigate')
    # gpio.setmode(gpio.BCM)

    pyrigate.log('Loading settings')
    load_settings()

    pyrigate.log('Loading plant configurations')
    pyrigate.load_configs()
    pyrigate.log('Loaded {0} plant configuration(s)', len(get_configs()),
                 verbosity=2)

    for config in configs:
        pyrigate.log("Loaded config for '{0}'", config['name'])


def send_status_report():
    pyrigate.output('TODO: Send status report')


def schedule_tasks():
    """Schedule status reports, watering plans etc."""
    if pyrigate.settings['status_updates']:
        schedule.every().saturday.at('10:00').do(send_status_report)


def quit():
    """Quit pyrigate."""
    # gpio.cleanup()
    log("Quitting pyrigate")


def run(args):
    """Runner function for pyrigate."""
    # if args['-v'] or args['--version']:
    #     sys.exit(all_versions())

    pyrigate.start()
    pyrigate.schedule_tasks()
    pyrigate.log('Running pyrigate')
    interpreter = pyrigate.command.CommandInterpreter()

    try:
        while True:
            # TODO: Monitor plants, water them etc.
            interpreter.cmdloop()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        # Catch any other error, log it and reraise it
        pyrigate.error(None, e.message)
        raise
    finally:
        pyrigate.quit()
