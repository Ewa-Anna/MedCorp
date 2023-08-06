from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField, SelectField
from wtforms.validators import InputRequired, Email, \
    Length, EqualTo, DataRequired
from wtforms.widgets import TextArea


from datetime import date, timedelta

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[
                             InputRequired(),
                             Length(min=6, max=20,
                                    message="Password must be \
                                    between 6 and 20 characters long.")])
    confirm_password = PasswordField("Confirm your password", validators=[
                                     InputRequired(),
                                     EqualTo("password",
                                             message="Your \
                                             passwords are not matching.")])
    submit = SubmitField("Register")


class RestorePassword(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Restore password")


class ChangePassword(FlaskForm):
    old_password = PasswordField("Old Password", validators=[InputRequired()])
    new_password = PasswordField("New Password", validators=[
                             InputRequired(),
                             Length(min=6, max=20,
                                    message="Password must be \
                                    between 6 and 20 characters long.")])
    confirm_password = PasswordField("Confirm your password", validators=[
                                     InputRequired(),
                                     EqualTo("new_password",
                                             message="Your \
                                             passwords are not matching.")])
    submit = SubmitField("Change password")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    subject = StringField("Subject", validators=[DataRequired()])
    body = StringField("Text", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField("Send message")


class EditProfile(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    birthdate = DateField("Birthdate", format='%Y-%m-%d')
    email = StringField("Email", validators=[InputRequired(), Email()])
    telephone = StringField("Telephone", validators=[InputRequired(),
                                                     Length(min=9, max=10,
                                                            message="Telephone number must be between 9 and 10 characters long.")])
    submit = SubmitField("Confirm")


class AddSpecialization(FlaskForm):
    specialization = StringField("Specialization", validators=[DataRequired()])
    submit = SubmitField("Add")


class EditUser(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    isAdmin = BooleanField("Admin")
    isDoctor = BooleanField("Doctor")
    isPatient = BooleanField("Patient")
    isActive = BooleanField("Active")
    specialization = SelectField("Specialization")
    submit = SubmitField("Edit")


class BookApp(FlaskForm):
    submit = SubmitField("Book")


class CreateNewUser(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[
                             InputRequired(),
                             Length(min=6, max=20,
                                    message="Password must be \
                                    between 6 and 20 characters long.")])
    confirm_password = PasswordField("Confirm your password", validators=[
                                     InputRequired(),
                                     EqualTo("password",
                                             message="Your \
                                             passwords are not matching.")])
    isAdmin = BooleanField("Admin")
    isDoctor = BooleanField("Doctor")
    isPatient = BooleanField("Patient")
    isActive = BooleanField("Active")
    submit = SubmitField("Create User")