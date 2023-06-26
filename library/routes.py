from flask import Flask, render_template, Blueprint, request, session, flash
from forms import MakeAppointment, ContactForm
from flask_login import login_required, current_user

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

@pages.route("/")
def home():
    return render_template("home.html")

@pages.route("/appointment", methods=["GET", "POST"])
@login_required
def appointment():
    form = MakeAppointment()
    if form.validate_on_submit():
        specialization = request.form["specialization"]
    return render_template("appointment.html", form=form)

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
