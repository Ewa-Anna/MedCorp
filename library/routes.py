from flask import Flask, render_template, Blueprint, request
from forms import MakeAppointment

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

@pages.route("/", methods = ["GET", "POST"])
def home():
    formAppointment = MakeAppointment()
    if formAppointment.validate_on_submit():
        specialization = request.form["specialization"]
        return render_template("home.html", form=formAppointment)

@pages.route("/login")
def login():
    return render_template("login.html")

@pages.route("/register")
def register():
    return render_template("register.html")

@pages.route("/about")
def about():
    return render_template("about.html")
