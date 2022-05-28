from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from docopt import docopt
import irc3

from . import config

usage = """
Usage: pinbot <config>

"""


def create():
    args = docopt(usage)

    settings = {
        "nick": "__pinbot__",
        "realname": "pinbot",
        "host": "irc.freenode.net",
        "port": 6667,
    }
    settings.update(config.resolve(args["<config>"]))

    bot = irc3.IrcBot(**settings)
    return bot
