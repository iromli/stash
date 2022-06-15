import os

import flask
import paypalrestsdk

DEBUG = True
SECRET_KEY = "RANDASDAD"

PAYPAL_MODE = os.environ.get("PAYPAL_MODE", "sandbox")

PAYPAL_CLIENT_ID = os.environ.get("PAYPAL_CLIENT_ID", "")

PAYPAL_CLIENT_SECRET = os.environ.get("PAYPAL_CLIENT_SECRET", "")

app = flask.Flask(__name__)
app.config.from_object(__name__)
paypalrestsdk.configure({
    "mode": app.config["PAYPAL_MODE"],
    "client_id": app.config["PAYPAL_CLIENT_ID"],
    "client_secret": app.config["PAYPAL_CLIENT_SECRET"],
    })


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/charge", methods=["POST"])
def charge():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {
                "total": "5",
                "currency": "USD",
                }
            }],
        "redirect_urls": {
            "return_url": flask.url_for(".process", _external=True),
            "cancel_url": flask.url_for(".index", _external=True),
            }
        })

    if payment.create():
        flask.session["payment_id"] = payment.id
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
        return flask.redirect(redirect_url)
    else:
        print(payment.error)
    return flask.redirect("/")


@app.route("/process")
def process():
    payment_id = flask.session["payment_id"]
    payer_id = flask.request.args["PayerID"]
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return flask.render_template("charge.html")
    return flask.redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
