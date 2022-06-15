from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import braintree

BRAINTREE_ENVIRONMENT_MAP = {
    "sandbox": braintree.Environment.Sandbox,
    "production": braintree.Environment.Production,
}


def _include_braintree(obj):
    for name, cls in braintree.__dict__.items():
        if name.islower():
            continue
        setattr(obj, name, cls)


class Braintree(object):
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)
        _include_braintree(self)

    def init_app(self, app):
        app.config.setdefault("BRAINTREE_MERCHANT_ID", "")
        app.config.setdefault("BRAINTREE_PUBLIC_KEY", "")
        app.config.setdefault("BRAINTREE_PRIVATE_KEY", "")
        app.config.setdefault("BRAINTREE_ENVIRONMENT", "sandbox")

        app.extensions = getattr(app, "extensions", {})
        app.extensions["braintree"] = self
        self.app = app

        env_name = self.app.config.get("BRAINTREE_ENVIRONMENT")
        env = BRAINTREE_ENVIRONMENT_MAP.get(env_name)
        assert env, "Missing or unsupported braintree environment."

        self.Configuration.configure(
            env,
            merchant_id=app.config["BRAINTREE_MERCHANT_ID"],
            public_key=app.config["BRAINTREE_PUBLIC_KEY"],
            private_key=app.config["BRAINTREE_PRIVATE_KEY"],
            )
