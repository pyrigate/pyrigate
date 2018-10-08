# -*- coding: utf-8 -*-

"""Interpreter class for user-entered commands."""

import cmd
import shlex

import pyrigate
import pyrigate.mail
from pyrigate.logging import output
from pyrigate.settings import get_settings


def print_dict(dictionary, indent=1):
    """Recursively print a dictionary."""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print("{0}: {1}".format(key, "\n"))
            print_dict(value, indent=indent+1)
        else:
            print("{0}: {1}".format(key, value))


def expect_args(command, args, count):
    """Check that a given command is given the argument count is expects."""
    if len(args) != count:
        output("Command '{0}' expected {1}", command,
               "{0} argument(s)".format(count) if count > 0
               else "no arguments")
        return False

    return True


class CommandInterpreter(cmd.Cmd, object):
    """Interpreter for user-entered commands."""

    def __init__(self, prompt='> '):
        super(CommandInterpreter, self).__init__()
        self.prompt = prompt

    def split_command(self, line):
        """Split a user-entered line into a command and its arguments."""
        tokens = shlex.split(line)

        return tokens[0], [] if len(tokens) == 1 else tokens[1:]

    def split_args(self, line):
        return shlex.split(line)

    def do_version(self, line):
        """Print pyrigate, python and raspberry pi versions."""
        output(pyrigate.all_versions())

    def do_reload(self, line):
        """Reload user settings."""
        get_settings().reload()
        output('Reloaded settings')

    def do_test_mail(self, line):
        """Test the mail system by sending a mail to the given address."""
        settings = get_settings()

        output("Sending mail to 'localhost'")
        output("From: {0}", settings['email']['sender'])
        output("To  : {0}", ", ".join(settings['email']['subscribers']))

        output("Start debug server 'sudo python2.7 -m smtpd -c"
               " DebuggingServer -n localhost:25' to see result")

        try:
            pyrigate.mail.send_mail(
                'Test',
                'pyrigate@gmail.com',
                ['albo.developer@gmail.com'],
                'Subject: Test\nThis is a test mail sent from pyrigate',
                port=25
            )  # , attachments=['coming_soon.png'])
        except TimeoutError:
            output("Operation timed out...")

    def do_pump(self, line):
        """Pump a specfic amount (dl, cm, ml etc.)."""
        args = self.split_args(line)

        if expect_args('pump', args, 2):
            pyrigate.get_pump(args[0]).pump(args[1])

    def do_water_level(self, line):
        """Query the water tank's current level."""
        args = self.split_args(line)
        lvl = pyrigate.get_pump(args[0]).level

        if lvl == -1:
            output("No water tank detected, cannot read water level")
        else:
            output("Current water level is {0}".format(lvl))

    def do_settings(self, line):
        """List current settings."""
        settings = get_settings()
        settings.list()

    def do_configs(self, line):
        """Print currently loaded plant configurations."""
        configs = pyrigate.get_configs()

        if not configs:
            output('No configurations loaded')
        else:
            output('Found {0} configuration(s):', len(configs))

            for config in configs:
                output("    * {0}", config['name'])

    def do_list(self, line):
        """List a configuration."""
        args = self.split_args(line)

        if expect_args('list', args, 1):
            config = next((c for c in pyrigate.get_configs()
                           if c['name'] == args[0]), None)

            if config is not None:
                config.list()

    def do_select(self, line):
        """Select the plant configuration to use."""
        args = self.split_args(line)

        if expect_args('select', args, 1):
            output("Selected plant configuration '{0}'"
                   .format(args[0]))

    def do_specs(self, line):
        """Print the Raspberry Pi's specifications."""
        for key, value in pyrigate.rpi_specs().items():
            print("{0:<20} {1}".format(key, value))

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
