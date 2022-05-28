from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
import os

import pytest
import six


@pytest.mark.parametrize("envvar,val,resolved", [
    ("PINBOT_HOST", "localhost", True),
    ("HOST", "localhost", False),
])
def test_get_envvars(envvar, val, resolved):
    from pinbot.core.config import get_envvars

    os.environ[envvar] = val
    assert (envvar in get_envvars()) == resolved


def test_resolve(tmpdir):
    from pinbot.core.config import resolve

    file_ = tmpdir.mkdir("pinbot_test").join("pinbot.ini")
    file_.write("""
    [bot]
    host = localhost
    port = 6667
    ssl = false
    async = true
    includes =
        custom.plugin

    [custom.plugin]
    name = ${ENV:PLUGIN_NAME}
    """)

    os.environ["PINBOT_PLUGIN_NAME"] = "custom"
    settings = resolve(six.text_type(file_))

    assert "host" in settings
    assert settings["port"] == 6667
    assert settings["ssl"] is False
    assert settings["async"] is True
    assert settings["includes"] == ["custom.plugin"]
    assert settings["custom.plugin"]["name"] == "custom"
