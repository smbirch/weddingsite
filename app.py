import os

from flask import Flask, render_template, request, redirect, flash
from forms import ContactForm
from flask_mail import Mail, Message
from dotenv import load_dotenv
import random
import logging

logger = logging.getLogger("weddingsite")
formatter = logging.Formatter(
    f"%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%m/%d/%Y %I:%M:%S %p"
)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# logging.basicConfig(
#     filename="logs.log",
#     level=logging.INFO,
#     disable_existing_loggers=True,
#     format=f"%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     datefmt="%m/%d/%Y %I:%M:%S %p",
# )


load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("app_secret_key")


mail = Mail()
app.config["MAIL_SERVER"] = "smtp.office365.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("mail_account")
app.config["MAIL_PASSWORD"] = os.getenv("email_password")
mail.init_app(app)


@app.route("/")
def index():
    ipaddr = request.environ.get("do-connecting-ip", request.remote_addr)
    logger.info(f"/homepage : {ipaddr}")
    return render_template("index.html")


@app.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    ipaddr = request.environ.get("do-connecting-ip", request.remote_addr)
    form = ContactForm()
    if request.method == "POST":
        if form.validate() == False:
            flash("All fields are required")
            return render_template("rsvp.html", form=form)
        else:
            msg = Message(
                subject=f"RSVP from {form.email.data}: {form.rsvp.data}",
                recipients=["birchwedding@outlook.com"],
                body=f"From: {form.name.data}\nEmail: {form.email.data}\nRSVP: {form.rsvp.data}",
                sender="birchwedding@outlook.com",
            )

            mail.send(msg)
            logger.info(f"formsubmit : {ipaddr}")
            if form.rsvp.data == "No":
                return redirect("livestream")

            else:
                logger.info(f"formsubmit : {ipaddr}")
                return redirect("thanks")

    elif request.method == "GET":
        logger.info(f"/rsvp : {ipaddr}")
        return render_template("rsvp.html", form=form)


@app.route("/info")
def info():
    ipaddr = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    logger.info(f"/info : {ipaddr}")
    return render_template("info.html")


@app.route("/thanks")
def thanks():
    return render_template("thanks.html")


@app.route("/livestream")
def livestream():
    return render_template("livestream.html")


@app.route("/gallery")
def gallery():
    ipaddr = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    logger.info(f"/gallery : {ipaddr}")
    photo_dir = os.path.dirname("static/images")
    photo_count = len(
        [
            name
            for name in os.listdir(photo_dir)
            if os.path.isfile(os.path.join(photo_dir, name))
        ]
    )

    random_photos = random.sample(range(1, 114), 16)

    return render_template("gallery.html", random_photos=random_photos)
