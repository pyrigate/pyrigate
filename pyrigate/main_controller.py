#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main controller for running the event loop and scheduling tasks."""

import os
from pathlib import Path
import schedule
import schema
import threading

import pyrigate
import pyrigate.command
import pyrigate.gpio as gpio
from pyrigate.config import PlantConfiguration
from pyrigate.decorators import configurable
from pyrigate.log import setup_logging, error, log, output
from pyrigate.pump import Pump
from pyrigate.sensor import Sensor
from pyrigate.user_settings import settings


# Adapted from run_continuously at
# https://github.com/mrhwick/schedule/blob/master/schedule/__init__.py
class ScheduleThread(threading.Thread):

    """Thread class for continuously running scheduled tasks."""

    def __init__(self, interval, event):
        self._interval = interval
        self._event = event
        super().__init__()

    def run(self):
        while True:
            schedule.run_pending()

            if self._event.wait(timeout=self._interval):
                break


class MainController(object):

    """Main controller for pyrigate."""

    def __init__(self):
        """Initialise the controller."""
        self._configs = []
        self._pumps = {}
        self._sensors = {}
        self._event = None

    def load_configs(self, config_path):
        """Load all configuration files found at the given path."""
        log('Loading plant configurations')
        config_ext = PlantConfiguration.extension()

        for dirpath, _, filenames in os.walk(config_path):
            for name in filenames:
                full_path = dirpath / Path(name)

                if full_path.suffix[1:] == config_ext:
                    try:
                        config = PlantConfiguration(full_path)
                        log("Config '{0}' from '{1}': "
                            "{{fg=green,bold}}✔{{reset}}", config.name,
                            full_path)
                        self._configs.append(config)
                    except schema.SchemaError as ex:
                        errors = [e for e in ex.autos + ex.errors if e]

                        log("Config '{0}': {{fg=red,bold}}✗{{reset}} "
                            "(reason: {1})", full_path, ','.join(errors))

        log('Loaded {0} plant configuration(s)', len(self.configs),
            verbosity=2)

    def load_pumps(self):
        """Load all pumps from settings."""
        for pump_name in settings['pumps']:
            values = settings['pumps'][pump_name]
            self._pumps[pump_name] = Pump(pump_name, values['pin'],
                                          values['flow_rate'])

        return True

    def load_sensors(self):
        """Load all sensors from settings."""
        for sensor_name in settings['sensors']:
            values = settings['sensors'][sensor_name]
            self._sensors[sensor_name] = Sensor(sensor_name,
                                                values['pin'],
                                                values['threshold'],
                                                values['analog'])

        return True

    @property
    def configs(self):
        """Return a list of loaded plant configurations."""
        return self._configs

    @property
    def pumps(self):
        """Return a list of all registered pumps."""
        return self._pumps

    def get_pump(self, name):
        """Return a pump by name or None."""
        return self.pumps.get(name, None)

    @property
    def sensors(self):
        """Return a list of all registered sensors."""
        return self._sensors

    def get_sensor(self, name):
        """Return a sensor by name or None."""
        return self.sensors.get(name, None)

    def start(self):
        """Start the main controller and the event loop."""
        setup_logging()
        log('Starting pyrigate')
        self.load_configs('./configs')
        self.load_pumps()
        self.load_sensors()
        gpio.init()

    def run(self):
        """Run the main controller and accept user input."""
        self.start()
        # self.schedule_tasks()

        log('Running pyrigate')
        output("Type 'help' for information")

        interpreter = pyrigate.command.CommandInterpreter(self)

        try:
            while True:
                # TODO: Monitor plants, water them etc.
                interpreter.cmdloop()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            # Catch any other error, log it and reraise it
            error(None, str(e))
            raise
        finally:
            self.quit()

    def quit(self):
        """Quit pyrigate."""
        log('Cancelling remaining tasks', verbosity=2)
        self.cancel_tasks()
        gpio.cleanup()
        log('Quitting pyrigate')

    @configurable('status_updates')
    def send_status_report():
        output('TODO: Send status report')

    def schedule_tasks(self):
        """Schedule status reports, watering plans etc."""
        if settings['send_status_report']:
            log('Scheduling status report', verbosity=2)
            schedule.every().saturday.at('10:00').do(self.send_status_report)

        # Schedule according to the current plant configuration
        config = self.current_config

        if config.scheme == 'auto':
            # Water plants automatically based on a water humidity sensor
            pass
        elif config.scheme == 'schedule':
            # Water plants at set intervals
            job = getattr('saturday', schedule.every())

            for timepoint in config.times:
                job = job.at(timepoint)
        elif config.scheme == 'periodically':
            # Water plants periodically e.g. every Saturday at 9:00AM
            pass

        def test_do():
            print("Hello")

        job.do(test_do)
        self._event = threading.Event()
        self._schedule_thread = ScheduleThread(1, self._event)

        log("Scheduling configuration '{0}'".format(self.current_config.name),
            verbosity=2)

    def cancel_tasks(self):
        """Cancel all running plant monitoring tasks."""
        if self._event:
            self._event.set()

            if self._schedule_thread:
                self._schedule_thread.join()
