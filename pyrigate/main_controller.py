#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main controller for running the event loop and scheduling tasks."""

import json
import os
from pathlib import Path
import schedule
import schema

import pyrigate
import pyrigate.command
import pyrigate.gpio as gpio
from pyrigate.config import ConfigError, PlantConfiguration
from pyrigate.decorators import configurable
from pyrigate.jobs import Job, StatusReportJob, WateringJob
from pyrigate.log import setup_logging, error, log, output, warn
from pyrigate.pump import Pump
from pyrigate.schedule_thread import ScheduleThread
from pyrigate.sensor import Sensor
from pyrigate.user_settings import settings


class MainController(object):
    """Main controller for pyrigate."""

    def __init__(self, args={}):
        """Initialise the controller, possibly with commandline arguments."""
        self._args = args
        self._configs = {}
        self._current_config = None
        self._pumps = {}
        self._sensors = {}
        self._schedule_thread = None

        if self._args['-v'] > 0:
            settings['verbosity'] = self._args['-v']

    def load_configs(self, config_path):
        """Load all configuration files found at the given path."""
        if self._args['--no-load-configs']:
            return

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

                        if config.name in self._configs:
                            raise ConfigError(
                                "Configuration with name '{}' already exists"
                                .format(config.name)
                            )

                        self._configs[config.name] = config
                    except schema.SchemaError as ex:
                        errors = [e for e in ex.autos + ex.errors if e]

                        log("Config '{0}' from '{1}': "
                            "{{fg=red,bold}}✗{{reset}} "
                            "(reason: {2})", config.name, full_path,
                            ','.join(errors))
                    except json.decoder.JSONDecodeError as ex:
                        log("Config '{0}' from '{1}': "
                            "{{fg=red,bold}}✗{{reset}} "
                            "(reason: {2})", config.name, full_path,
                            ex)
                    except ConfigError as ex:
                        error(ConfigError, str(ex))
                        return False

        log('Loaded {0} plant configuration(s)', len(self.configs),
            verbosity=2)

        return True

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
    def current_config(self):
        """Return the currently selected configuration."""
        return self._current_config

    def select_config(self, config_name):
        """."""
        self._current_config = self.configs[config_name]

    @property
    def pumps(self):
        """Return a list of all registered pumps."""
        return self._pumps.values()

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
        gpio.init()

        return self.load_configs('./configs')\
            and self.load_pumps()\
            and self.load_sensors()

    def run(self):
        """Run the main controller and accept user input."""
        if not self.start():
            self.quit()
            return
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
        self.cancel_tasks()
        gpio.cleanup()
        log('Quitting pyrigate')

    @configurable('status_updates')
    def send_status_report(self):
        output('TODO: Send status report')

    def schedule_tasks(self):
        """Schedule status reports, watering plans etc."""
        # Schedule according to the current plant configuration
        if not self.current_config:
            warn('No configuration selected, no schedules started')
            return

        config = self.configs['Serrano']
        # config = self.current_config
        # print(config)

        # watering_job = WateringJob(config['scheme'])
        # watering_job.schedule()
        # report_job = StatusReportJob(settings)
        # report_job.schedule()

        class TestJob(pyrigate.jobs.job.Job):
            def schedule(self):
                schedule.every(3).seconds.do(self.do)

            def do(self):
                log('Hello from TestJob')

        job = TestJob()
        job.schedule()

        # if settings['status_updates']:
        report_job = StatusReportJob(settings['status_frequency'])
        report_job.schedule()

        self._schedule_thread = ScheduleThread(1)
        self._schedule_thread.start()

        log("Scheduling configuration '{0}'".format(config.name), verbosity=2)

    def cancel_tasks(self):
        """Cancel all running plant monitoring tasks."""
        if self._schedule_thread:
            log('Cancelling remaining tasks', verbosity=2)
            self._schedule_thread.cancel()
