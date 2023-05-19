from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email


class DoctorsList(FlaskForm):
    dropdowns = 10
    doctors = SelectField("Doctors", validators=[InputRequired()])


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")
