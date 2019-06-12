#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main runner for pyrigate."""

import docopt
import pyrigate
from pyrigate.main_controller import MainController


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


if __name__ == "__main__":
    MainController().run()
