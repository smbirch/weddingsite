from flask import Flask, render_template, request
from forms import ContactForm

app = Flask(__name__)
app.secret_key = "development key"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    form = ContactForm()

    if request.method == "POST":
        return "form posted"
    return render_template("rsvp.html", form=form)


@app.route("/info")
def info():
    return render_template("info.html")
