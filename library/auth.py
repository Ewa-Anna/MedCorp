from flask import Flask, render_template, Blueprint, request, session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
from models import User
from flask_login import login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy

authorize = Blueprint(
    "authorize", __name__, template_folder="templates", static_folder="static"
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@authorize.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

@authorize.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Email or password is not correct.")
        return redirect(url_for("auth.login"))
    
    login_user(user, remember=remember)
    return redirect(url_for("pages.home"))

@authorize.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@authorize.route("/register", methods=["POST"])
def register_post():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user:
        flash("User already exists.")
        return redirect("auth.login")
    
    new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("home"))

@authorize.route("/logout")
@login_required
def logout():
    login_user()
    session.clear()
    return render_template("home.html")

