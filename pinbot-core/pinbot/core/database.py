from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import dataset
import irc3


@irc3.plugin
class Dataset(object):
    def __init__(self, bot):
        self.bot = bot
        self._db = None

        config = {"url": "sqlite:///pinbot.db"}
        config.update(self.bot.config.get(__name__, {}))
        self.config = config

    @property
    def db(self):
        if self._db is None:
            self._db = dataset.connect(self.config["url"])
        return self._db
