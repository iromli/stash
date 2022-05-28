from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


def test_dataset():
    import os
    import sys
    from pinbot.core.bot import create
    from pinbot.core.database import Dataset

    os.environ["PINBOT_HOST"] = "127.0.0.1"
    os.environ["PINBOT_INCLUDES"] = "pinbot.core.database"
    os.environ["PINBOT_DATABASE_URL"] = "sqlite://"

    sys.argv = ["pinbot", "bot.ini"]
    bot = create()
    dataset = Dataset(bot)
    assert dataset.db is not None
