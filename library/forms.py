from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired
from wtforms.widgets import TextArea


class MakeAppointment(FlaskForm):
    dropdowns = 10
    specialization = SelectField(
        "Choose a specialization", choices=[], validators=[InputRequired()])
    submit = SubmitField("Show available doctors")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[
                             InputRequired(),
                             Length(min=6, max=20, message="Password must be between 6 and 10 characters long.")])
    confirm_password = PasswordField("Confirm your password", validators=[
                                     InputRequired(), EqualTo("password", message="Your passwords are not matching.")])
    submit = SubmitField("Register")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    subject = StringField("Subject", validators=[DataRequired()])
    body = StringField("Text", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField("Send message")

