#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main runner for pyrigate."""

import docopt
import pyrigate
from pyrigate.main_controller import MainController


def parse_commandline():
    options = """Usage:
    pyrigate [-v...] [-x | --no-load-configs]

    Options:
        -h, --help              Display this help message.
        --version               Display the pyrigate, Python and Raspberry Pi
                                versions.
        -v                      Increase verbosity level (output). Zero
                                silences all output [default: 1]. Overrides the
                                verbosity set in user settings.
        -x, --no-load-configs   Do not load any configurations on start-up.

    """

    return docopt.docopt(options, version=pyrigate.all_versions())


def main():
    MainController(parse_commandline()).run()


if __name__ == "__main__":
    main()
