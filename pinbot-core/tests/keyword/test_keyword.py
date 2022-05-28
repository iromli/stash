from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import irc3.testing
import irc3.utils
import pytest


@pytest.fixture(scope="function")
def bot(request):
    settings = {
        "host": "localhost",
        "includes": ["pinbot.keyword"],
        "pinbot.core.database": {
            "url": "sqlite://",
        },
        "autojoins": ["pinbot"],
        "testing": True,
    }

    bot = irc3.testing.IrcBot(**settings)
    return bot


@pytest.fixture(scope="function")
def plugin(request, bot):
    from pinbot.keyword import Keyword

    plugin = Keyword(bot)
    return plugin


def test_db(plugin):
    assert plugin.db is not None


def test_remember_succeed(bot, plugin):
    mask = irc3.utils.IrcString("foo!foo@localhost")
    target = bot.config["autojoins"][0]
    args = {"<keyword>": "foo", "<contents>": ["bar"], "remember": True}

    bot.protocol.write.reset_mock()
    plugin.remember(mask, target, args)

    bot.protocol.write.assert_called_once_with(
        "PRIVMSG pinbot :thanks {}, it's good to know".format(mask.nick)
    )


def test_remember_failed(bot, plugin):
    mask = irc3.utils.IrcString("foo!foo@localhost")
    target = bot.config["autojoins"][0]
    args = {"<keyword>": "foo", "<contents>": ["bar"], "remember": True}

    plugin.remember(mask, target, args)
    bot.protocol.write.reset_mock()

    plugin.remember(mask, target, args)
    bot.protocol.write.assert_called_once_with(
        "PRIVMSG pinbot :sorry {}, {} is exist".format(
            mask.nick, args["<keyword>"])
    )


def test_whatis_succeed(bot, plugin):
    mask = irc3.utils.IrcString("foo!foo@localhost")
    target = bot.config["autojoins"][0]
    args = {"<keyword>": "foo", "<contents>": ["bar"], "remember": True}

    plugin.remember(mask, target, args)
    bot.protocol.write.reset_mock()

    args = {"<keyword>": "foo", "whatis": True}
    plugin.whatis(mask, target, args)
    bot.protocol.write.assert_called_once_with(
        "PRIVMSG pinbot :{}, {} is {}".format(
            mask.nick, args["<keyword>"], "bar")
    )


def test_whatis_failed(bot, plugin):
    mask = irc3.utils.IrcString("foo!foo@localhost")
    target = bot.config["autojoins"][0]
    args = {"<keyword>": "foo", "whatis": True}

    bot.protocol.write.reset_mock()
    plugin.whatis(mask, target, args)

    bot.protocol.write.assert_called_once_with(
        "PRIVMSG pinbot :sorry {}, i don't know what {} is".format(
            mask.nick, args["<keyword>"])
    )


def test_tell_succeed(bot, plugin):
    mask = irc3.utils.IrcString("foo!foo@localhost")
    target = bot.config["autojoins"][0]
    args = {"<keyword>": "foo", "<contents>": ["bar"], "remember": True}

    plugin.remember(mask, target, args)
    bot.protocol.write.reset_mock()

    args = {"<keyword>": "foo", "<nick>": "smith", "tell": True}
    plugin.tell(mask, target, args)
    bot.protocol.write.assert_called_once_with(
        "PRIVMSG pinbot :{}, {} is {}".format(
            args["<nick>"], args["<keyword>"], "bar")
    )


def test_tell_failed(bot, plugin):
    mask = irc3.utils.IrcString("foo!foo@localhost")
    target = bot.config["autojoins"][0]
    args = {"<keyword>": "foo", "<nick>": "smith", "tell": True}

    bot.protocol.write.reset_mock()
    plugin.tell(mask, target, args)

    bot.protocol.write.assert_called_once_with(
        "PRIVMSG pinbot :sorry {}, i don't know what {} is".format(
            mask.nick, args["<keyword>"])
    )


def test_forget_succeed(bot, plugin):
    mask = irc3.utils.IrcString("foo!foo@localhost")
    target = bot.config["autojoins"][0]
    args = {"<keyword>": "foo", "<contents>": ["bar"], "remember": True}

    plugin.remember(mask, target, args)
    bot.protocol.write.reset_mock()

    args = {"<keyword>": "foo", "forget": True}
    plugin.forget(mask, target, args)
    bot.protocol.write.assert_called_once_with(
        "PRIVMSG pinbot :ok {}".format(mask.nick)
    )


def test_forget_failed(bot, plugin):
    mask = irc3.utils.IrcString("foo!foo@localhost")
    target = bot.config["autojoins"][0]
    args = {"<keyword>": "foo", "tell": True}

    bot.protocol.write.reset_mock()
    plugin.forget(mask, target, args)

    bot.protocol.write.assert_called_once_with(
        "PRIVMSG pinbot :sorry {}, i don't know what {} is".format(
            mask.nick, args["<keyword>"])
    )
