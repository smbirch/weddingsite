from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])

    email = StringField("Email", validators=[DataRequired(), Email()])

    rsvp = RadioField(
        "Will you be in attendance?",
        choices=["Yes", "No"],
        validators=[InputRequired()],
    )

    submit = SubmitField("Submit")
