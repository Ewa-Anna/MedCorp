from flask import Flask, render_template, Blueprint, request, session
from forms import MakeAppointment, LoginForm, RegisterForm

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages.route("/", methods=["GET", "POST"])
def home():
    form = MakeAppointment()
    if form.validate_on_submit():
        specialization = request.form["specialization"]
        return render_template("home.html", form=form)


@pages.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@pages.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)


@pages.route("/logout")
def logout():
    session.clear()
    return render_template("home.html")


@pages.route("/about")
def about():
    return render_template("about.html")

@pages.route("/contact")
def contact():
    return render_template("contact.html")
