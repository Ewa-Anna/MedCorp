from flask import Flask, render_template, Blueprint, request, session, flash, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
from models import User
from flask_login import login_user, login_required, logout_user
from datetime import datetime
from db import db
from valid import isProperMail

authorize = Blueprint(
    "authorize", __name__, template_folder="templates", static_folder="static"
)

@authorize.route("/login", methods=["GET"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

@authorize.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()
    session["logged_in"] = True
    
    if not user or not check_password_hash(user.password, password):
        flash("Email or password is not correct.")
        return redirect(url_for("authorize.login"))
    
    login_user(user, remember=remember)

    return redirect(url_for("pages.home"))

@authorize.route("/register", methods=["GET"])
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)

@authorize.route("/register", methods=["POST"])
def register_post():
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    isAdmin = False
    isDoctor = False
    isPatient = True
    isActive = True

    user = User.query.filter_by(email=email).first()

    if user:
        flash("User already exists.")
        return redirect("authorize.login")
    
    if not isProperMail(email):
        flash("Please provide correct email address.")
        return redirect("authorize.login")

    if password != confirm_password:
        flash("Passwords are not matching.")
        return render_template("register.html")

    new_user = User(email=email, password=generate_password_hash(password, method='sha256'), isAdmin=isAdmin, isDoctor=isDoctor, isPatient=isPatient, isActive=isActive)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("authorize.login"))

@authorize.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return render_template("home.html")

