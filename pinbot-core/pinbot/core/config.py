from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import os

import irc3.utils
import configparser


def get_envvars():
    return {
        k: v for k, v in os.environ.items()
        if k.startswith("PINBOT_")
    }


def resolve(file_):
    parser = configparser.SafeConfigParser(
        interpolation=configparser.ExtendedInterpolation())
    parser.read(file_)

    parser.add_section("ENV")
    for k, v in get_envvars().items():
        parser.set("ENV", k.replace("PINBOT_", ""), v)

    settings = {}
    for s in parser.sections():
        items = {}
        for k, v in parser.items(s):
            if "\n" in v:
                v = irc3.utils.as_list(v)
            elif v.isdigit():
                v = int(v)
            elif v == "true":
                v = True
            elif v == "false":
                v = False
            items[k] = v
        settings[s] = items

    settings.pop("ENV", None)
    settings.update(settings.pop("bot", {}))
    return settings
