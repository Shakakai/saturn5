#!/usr/bin/env python
"""
saturn5: A Django Development CLI
Usage: saturn5 <command>

Commands:
    check
    run
    new
    shell
    help
    version
"""

import docopt
import sys

from saturn5 import runner
from saturn5 import __version__

VALID_ACTIONS = [
    "check",
    "run",
    "new",
    "shell",
    "help",
    "version"
]


def run():
    args = docopt.docopt(__doc__)
    command = args["<command>"]
    if command not in VALID_ACTIONS:
        print("Invalid command.")
        return sys.exit(1)

    if command == "help":
        print(__doc__)
        return sys.exit(0)

    if command == "version":
        print(__version__)
        return sys.exit(0)

    if not getattr(runner, command)():
        return sys.exit(1)
    return sys.exit(0)

