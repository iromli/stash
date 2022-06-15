import os

import flask
import stripe

DEBUG = True
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")

app = flask.Flask(__name__)
app.config.from_object(__name__)
stripe.api_key = app.config["STRIPE_SECRET_KEY"]


@app.route("/")
def index():
    return flask.render_template(
        "index.html", key=app.config["STRIPE_PUBLISHABLE_KEY"])


@app.route("/charge", methods=["POST"])
def charge():
    # amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email="customer@example.com",
        card=flask.request.form["stripeToken"],
        )

    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency="usd",
        description="Flask charge",
        )

    return flask.render_template("charge.html", amount=amount)


if __name__ == "__main__":
    app.run()
