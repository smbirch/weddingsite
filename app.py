import config

from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = config.app_secret_key


mail = Mail()
app.config["MAIL_SERVER"] = "smtp.office365.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = "birchwedding@outlook.com"
app.config["MAIL_PASSWORD"] = config.email_password
mail.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    form = ContactForm()
    if request.method == "POST":
        if form.validate() == False:
            flash("All fields are required")
            return render_template("rsvp.html", form=form)
        else:
            msg = Message(
                form.subject.data,
                sender="birchwedding@outlook.com",
                recipients=["birchwedding@outlook.com"],
            )
            msg.body = """From: %s <%s>%s""" % (
                form.name.data,
                form.email.data,
                form.message.data,
            )
            mail.send(msg)
            return render_template("rsvp.html", success=True)
    elif request.method == "GET":
        return render_template("rsvp.html", form=form)


@app.route("/info")
def info():
    return render_template("info.html")
