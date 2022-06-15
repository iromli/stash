from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from flask import Flask
from flask import render_template
from flask import request
from flask_braintree import Braintree

DEBUG = True
BRAINTREE_MERCHANT_ID = os.environ.get("BRAINTREE_MERCHANT_ID", "")
BRAINTREE_PUBLIC_KEY = os.environ.get("BRAINTREE_PUBLIC_KEY", "")
BRAINTREE_PRIVATE_KEY = os.environ.get("BRAINTREE_PRIVATE_KEY", "")

app = Flask(__name__)
app.config.from_object(__name__)

braintree = Braintree()
braintree.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/transaction")
def start_transaction():
    return render_template("transaction.html")


@app.route("/create_transaction", methods=["POST"])
def create_transaction():
    result = braintree.Transaction.sale({
        "amount": "1000.00",
        "credit_card": {
            "number": request.form["number"],
            "cvv": request.form["cvv"],
            "expiration_month": request.form["month"],
            "expiration_year": request.form["year"]
        },
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success:
        return "<h1>Success! Transaction ID: {0}</h1>".format(result.transaction.id)  # noqa
    else:
        return "<h1>Error: {0}</h1>".format(result.message)


if __name__ == "__main__":
    app.run()
