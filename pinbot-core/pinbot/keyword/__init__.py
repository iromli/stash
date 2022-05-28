from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import irc3
from irc3.plugins.command import command


@irc3.plugin
class Keyword(object):

    requires = [
        "irc3.plugins.command",
        "pinbot.core.database",
    ]

    def __init__(self, bot):
        self.bot = bot

    @property
    def db(self):
        imp_string = "pinbot.core.database.Dataset"
        mod_name, obj_name = imp_string.rsplit(".", 1)
        mod = __import__(mod_name, None, None, [obj_name])
        return self.bot.get_plugin(getattr(mod, obj_name)).db

    @command(permission="keyword")
    def remember(self, mask, target, args):
        """Remembers a keyword.

        %%remember <keyword> is <contents>...
        """
        row = self.db["keywords"].find_one(keyword=args["<keyword>"],
                                           channel=target)

        if row:
            msg = "sorry {0}, {1} is exist".format(
                mask.nick, args["<keyword>"])
        else:
            self.db["keywords"].insert({
                "keyword": args["<keyword>"],
                "user": mask.nick,
                "channel": target,
                "contents": " ".join(args["<contents>"]),
                })
            msg = "thanks {0}, it's good to know".format(mask.nick)
        self.bot.privmsg(target, msg)

    @command()
    def whatis(self, mask, target, args):
        """Finds a keyword.

        %%whatis <keyword>
        """
        row = self.db["keywords"].find_one(keyword=args["<keyword>"],
                                           channel=target)
        if not row:
            msg = "sorry {0}, i don't know what {1} is".format(
                mask.nick, args["<keyword>"])
        else:
            msg = "{0}, {1} is {2}".format(
                mask.nick, args["<keyword>"], row["contents"])
        self.bot.privmsg(target, msg)

    @command()
    def tell(self, mask, target, args):
        """Finds a keyword and tells to someone.

        %%tell <nick> about <keyword>
        """
        row = self.db["keywords"].find_one(keyword=args["<keyword>"],
                                           channel=target)
        if not row:
            msg = "sorry {0}, i don't know what {1} is".format(
                mask.nick, args["<keyword>"])
        else:
            msg = "{0}, {1} is {2}".format(
                args["<nick>"], args["<keyword>"], row["contents"])
        self.bot.privmsg(target, msg)

    @command(permission="keyword")
    def forget(self, mask, target, args):
        """Removes a keyword.

        %%forget <keyword>
        """
        deleted = self.db["keywords"].delete(keyword=args["<keyword>"],
                                             channel=target)
        if deleted:
            msg = "ok {}".format(mask.nick)
        else:
            msg = "sorry {0}, i don't know what {1} is".format(
                mask.nick, args["<keyword>"])
        self.bot.privmsg(target, msg)
