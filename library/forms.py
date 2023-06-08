from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email


class MakeAppointment(FlaskForm):
    dropdowns = 10
    specialization = SelectField("Choose a specialization", choices=[], validators=[InputRequired()])
    submit = SubmitField("Show available doctors")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")
