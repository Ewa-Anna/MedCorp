from flask import Flask, render_template, Blueprint, request, session, flash, abort
from forms import ContactForm
from flask_login import login_required, current_user
from mail import Message, mail
from models import User

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

@pages.route("/")
def home():
    return render_template("home.html")

@pages.route("/appointment", methods=["GET", "POST"])
@login_required
def appointment():
    with open("templates/specs.txt", "r") as f:
        specs = f.readlines()
    return render_template("appointment.html", specs=specs)

@pages.route("/profile/<int:_id>", methods=["GET", "POST"])
def profile(_id: int):
    profile_data = current_user.db.user.find_one({"_id": _id})
    if not profile_data:
        abort(404)
    profile = User(**profile_data)
    return render_template("profile.html", profile=profile)

@pages.route("/about")
def about():
    return render_template("about.html")

@pages.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if request.method == "POST":
        if form.validate() == False:
            flash("All fields are required.")
            return render_template("contact.html", form=form)
        else:
            msg = Message(form.subject.data, sender="example@example.com", recipients=["example@example.com"])
            msg.body = """ 
            From: %s &lt;%s&gt;
            %s 
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return "E-mail sent"
    elif request.method == "GET":
        return render_template("contact.html", form=form)
