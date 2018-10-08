#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main runner for pyrigate."""

import docopt
import pyrigate
import pyrigate.command
import pyrigate.config
import pyrigate.mail


def parse_commandline():
    options = """Usage:
    pyrigate [-v=<lvl>] [--verbosity=<lvl>]

    Options:
        -h, --help              Display this help message
        --version               Display the pyrigate, Python and Raspberry Pi
                                versions
        -v, --verbosity=<lvl>   Set the level of verbosity (output). Zero
                                silences all output

    """

    return docopt.docopt(options, version=pyrigate.all_versions())


def main():
    pyrigate.run(parse_commandline())
