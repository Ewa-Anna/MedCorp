from flask import (
    render_template,
    Blueprint,
    request,
    session,
    flash,
    redirect,
    url_for,
    abort,
)
from flask_login import login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash

from ..db.forms import LoginForm, RegisterForm, ChangePassword
from ..db.models import User, Profile
from ..db.db import db

from ..valid import isProperMail

authorize = Blueprint(
    "authorize", __name__, template_folder="templates", static_folder="static"
)


@authorize.route("/login", methods=["GET"])
def login():
    form = LoginForm()
    return render_template("auth/login.html", form=form)


@authorize.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Email or password is not correct.")
        return redirect(url_for(".login"))

    session["logged_in"] = True
    login_user(user, remember=remember)

    return redirect(url_for("pages.home"))


@authorize.route("/register", methods=["GET"])
def register():
    form = RegisterForm()
    return render_template("auth/register.html", form=form)


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
        return redirect(url_for(".login"))

    if not isProperMail(email):
        flash("Please provide correct email address.")
        return redirect(url_for(".register"))

    if password != confirm_password:
        flash("Passwords are not matching.")
        return render_template("auth/register.html")

    new_user = User(
        email=email,
        password=password,
        isAdmin=isAdmin,
        isDoctor=isDoctor,
        isPatient=isPatient,
        isActive=isActive,
    )
    profile = Profile(user=new_user, email=email)

    db.session.add(new_user)
    db.session.add(profile)
    db.session.commit()

    return redirect(url_for(".login"))


@authorize.route("/change_password/<int:_id>", methods=["GET", "POST"])
@login_required
def change_password(_id: int):
    form = ChangePassword()
    user = current_user

    if current_user._id != _id:
        abort(403)

    if request.method == "POST":
        user = current_user
        old_password = form.old_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        if not check_password_hash(user.password, old_password):
            flash("Incorrect old password.", "danger")
            return render_template("auth/change_password.html", form=form, user=user)

        if new_password == confirm_password:
            user.password = generate_password_hash(new_password, method="sha256")
            db.session.commit()
            flash("Password changed successfully", "success")
            return redirect(url_for("pages.profile", _id=_id, user=user))

        else:
            flash("Passwords do not match", "danger")
            return render_template("auth/change_password.html", form=form, user=user)

    return render_template("auth/change_password.html", form=form, user=user)


@authorize.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("pages.home"))
