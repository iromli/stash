import hashlib

import dataset
import sqlalchemy.exc
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import url_for
from flask import g
from flask.ext.babel import Babel
from flask.ext.login import LoginManager
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import current_user

DEBUG = True
BABEL_DEFAULT_LOCALE = "en"
BABEL_DEFAULT_TIMEZONE = "UTC"
SECRET_KEY = "usiyfd90wq38hjk"

app = Flask(__name__)
app.config.from_object(__name__)
babel = Babel(app)
login_manager = LoginManager(app)
db = dataset.connect("sqlite:///demo.db")


class User(object):
    def __init__(self, **props):
        for k, v in props.items():
            setattr(self, k, v)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False


def generate_password_hash(value):
    return hashlib.sha1(value).hexdigest()


@app.url_defaults
def add_language_code(endpoint, values):
    if "lang" in values or not g.current_locale:
        return

    if app.url_map.is_endpoint_expecting(endpoint, "lang"):
        values["lang"] = g.current_locale


@app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    if current_user and current_user.is_authenticated():
        fallback_locale = current_user.locale
    else:
        fallback_locale = None

    try:
        g.current_locale = values.pop("lang", fallback_locale)
    except AttributeError:
        g.current_locale = fallback_locale


@babel.localeselector
def get_locale():
    """Gets locale.

    Priorities:

    1. use global locale if using URL prefix
    2.
    """
    if g.current_locale:
        return g.current_locale

    if current_user and current_user.is_authenticated():
        return current_user.locale
    return request.accept_languages.best_match(["id", "en"])


@babel.timezoneselector
def get_timezone():
    if current_user and current_user.is_authenticated():
        return current_user.timezone


@login_manager.user_loader
def load_user(uid):
    return User(**db["users"].find_one(id=uid))


@app.route("/")
@app.route("/<lang>")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
@app.route("/<lang>/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        return redirect(url_for(".index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = db["users"].find_one(username=username)

        if user and user["password"] == generate_password_hash(password):
            login_user(User(**user))
            return redirect(url_for(".index"))
    return render_template("login.html")


@app.route("/logout")
@app.route("/<lang>/logout")
def logout():
    logout_user()
    g.current_locale = None
    return redirect(url_for(".index"))

if __name__ == "__main__":
    db.begin()
    try:
        db["users"].insert(dict(
            id=1,
            username="demo",
            password=generate_password_hash("demo1234"),
            locale="id",
            timezone="UTC+7",
        ))
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
    app.run()
