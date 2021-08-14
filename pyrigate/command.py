# -*- coding: utf-8 -*-

"""Interpreter for user-entered commands."""

import cmd
import colorise
import importlib
import shlex

import pyrigate
import pyrigate.gpio as gpio
import pyrigate.mail
from pyrigate.log import output, warn
from pyrigate.user_settings import settings
from pyrigate.utils.printing import print_dict, print_columns, print_list


class CommandInterpreter(cmd.Cmd):
    """Interpreter for user-entered commands."""

    def __init__(self, controller, prompt='> '):
        super(CommandInterpreter, self).__init__()
        self._controller = controller
        self.prompt = prompt

    def split_command(self, line):
        """Split a user-entered line into a command and its arguments."""
        tokens = shlex.split(line)

        return tokens[0], [] if len(tokens) == 1 else tokens[1:]

    def expect_args(self, command_name, command, count):
        """Check that a command is given the number of arguments it expects."""
        args = shlex.split(command)

        if len(args) != count:
            if count == 0:
                msg = "no arguments"
            elif count == 1:
                msg = '{0} argument'
            else:
                msg = '{0} arguments'

            output("Command '{0}' expected {1}",
                   command_name,
                   msg.format(count))
            return None

        return args[0] if count == 1 else args

    def columnise(self, mapping):
        """Print dictionary keys and values in two columns."""
        max_width = max(10, len(max(mapping, key=len)))

        for key in mapping:
            colorise.fprint('{{fg=white,bold}}{0:<{1}} {{reset}} {2}'
                            .format(key, max_width, mapping[key]))

    def do_version(self, line):
        """Print pyrigate, python and raspberry pi versions."""
        output(pyrigate.all_versions())

    def do_reload(self, line):
        """Reload user settings."""
        importlib.reload(pyrigate.user_settings)
        output('Reloaded settings')

    def do_test_mail(self, line):
        """Test the mail system by sending a mail to the given address."""
        if not settings['email']:
            output('Please set email settings to send test mail')
        elif not settings['email']['sender']:
            output('Please set email.sender to send test mail')
        elif not settings['email']['subscribers']:
            output('Please set email.subscribers to send test mail')
        else:
            output("Sending mail to 'localhost'")
            output("From: {0}", settings['email']['sender'])
            output("To  : {0}", ", ".join(settings['email']['subscribers']))
            output("Start debug server 'sudo python -m smtpd -c "
                   "DebuggingServer -n localhost:25' to see result")

            try:
                pyrigate.mail.send_mail(
                    'Test',
                    settings['email']['sender'],
                    settings['email']['subscribers'],
                    'Subject: Test\nThis is a test mail sent from pyrigate',
                    server='localhost',
                    port=25
                )
            except TimeoutError:
                output("Operation timed out...")

    def do_pump(self, line):
        """Pump a specfic amount (dl, cm, ml etc.).

        pump <name> <amount>

        You can also use 'on' and 'off' to control the pump.

        """
        args = self.expect_args('pump', line, 2)

        if args:
            pump = self._controller.get_pump(args[0])

            if not pump:
                warn('No pump with that name')
                return

            cmd = args[1].lower()

            if cmd == 'on':
                pump.activate()
                output("Pump '{0}' activated".format(pump.name))
            elif cmd == 'off':
                pump.deactivate()
                output("Pump '{0}' deactivated".format(pump.name))
            else:
                try:
                    pump.pump(float(args[1]))
                except ValueError:
                    warn(
                        "Cannot convert '{0}' to a floating-point value"
                        .format(args[1])
                    )

    def do_pumps(self, line):
        """Show all loaded pumps."""
        pumps = self._controller.pumps

        if pumps:
            self.columnise(pumps)
        else:
            print('No pumps loaded')

    def do_sensor(self, line):
        """Query the value of a sensor."""
        arg = self.expect_args('sensor', line, 1)
        sensor = self._controller.get_sensor(arg)

        if sensor:
            output('Current value is {0} (analog: {1})'
                   .format(sensor.read(), sensor.analog))
        else:
            output("No sensor called '{0}' registered".format(arg))

    def do_sensors(self, line):
        """."""
        if self._controller.sensors:
            self.columnise(self._controller.sensors)
        else:
            print('No sensors loaded')

    def do_settings(self, line):
        """List current settings."""
        print_dict(settings)

    def do_configs(self, line):
        """Print currently loaded plant configurations."""
        configs = self._controller.configs

        if not configs:
            output('No configurations loaded')
        else:
            print_columns(
                [[name, config.path] for name, config in configs.items()],
                headers=['Name', 'Path']
            )

    def do_config(self, line):
        """List a configuration."""
        arg = self.expect_args('config', line, 1)

        if arg:
            configs = self._controller.configs

            if arg in configs:
                config = configs[arg]

                print_list([
                    ('Name', config.name),
                    ('Description', config.description),
                    ('Path', config.path),
                    ('Pump', config.scheme['pump']),
                    ('Amount', config.scheme['amount']),
                    ('Schedule', config.schedule_description),
                    ('Running?', self._controller.is_job_running(arg)),
                ])
            else:
                print("Unknown plant configuration '{0}'".format(arg))

    def do_select(self, line):
        """Select the plant configuration to use."""
        arg = self.expect_args('select', line, 1)

        if arg:
            self._controller.select_config(arg)

            output("Selected plant configuration '{0}'".format(arg))

    def do_rpi_specs(self, line):
        """Print the Raspberry Pi's specifications."""
        if gpio.mocked():
            output(
                'Cannot get Raspberry Pi specs, gpio access is being mocked'
            )
        else:
            for key, value in pyrigate.rpi_specs().items():
                print("{0:<20} {1}".format(key, value))

    def do_read_pin(self, line):
        """Read a value from a gpio input pin."""
        arg = self.expect_args('read', line, 1)

        if arg:
            if gpio.mocked():
                output('Cannot read pin, gpio access is being mocked')
            else:
                pin = int(arg)
                output("Read value '{0}' from pin '{1}'", gpio.input(pin), pin)

    def do_write_pin(self, line):
        """Write a HIGH or LOW value to a gpio output pin."""
        args = self.expect_args('write', line, 2)

        if args:
            if gpio.mocked():
                output('Cannot write pin, gpio access is being mocked')
            else:
                pin = int(args[0])
                value = int(args[1])

                if pin in (gpio.LOW, gpio.HIGH):
                    output("Wrote '{0}' on pin '{1}'",
                           gpio.output(pin, value), pin)
                else:
                    output("Output value must be either '{0}' or '{1}'",
                           gpio.LOW, gpio.HIGH)

    def do_schedule(self, line):
        """Start all scheduled jobs such as the current plant configuration.

        > schedule [start | stop]

        """
        arg = self.expect_args('schedule', line, 1)

        if arg == 'start':
            self._controller.schedule_tasks()
        elif arg == 'stop':
            self._controller.cancel_tasks()
        else:
            output("Unknown arg '{}'".format(arg))

    def do_jobs(self, line):
        """List all running jobs."""
        jobs = self._controller.jobs

        if not jobs:
            output('No running jobs')
        else:
            for jobname in jobs:
                job = jobs[jobname]

                output(
                    "Job '{0}' runs {1} (runs: {2})",
                    jobname,
                    job.description,
                    job.runs
                )

    def do_quit(self, line):
        """Quit pyrigate."""
        raise KeyboardInterrupt

    def emptyline(self):
        """Do not repeat the last command, just prompt the user again."""
        pass

    def default(self, line):
        """Handle unknown commands."""
        command, args = self.split_command(line)

        args = "" if not args\
            else " with argument(s) {0}".format(", ".join(args))

        output("Unrecognised command '{0}'{1}".format(command, args))
