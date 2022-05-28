def test_create():
    import sys
    from pinbot.core.bot import create

    sys.argv = ["pinbot", "bot.ini"]
    bot = create()
    assert bot
