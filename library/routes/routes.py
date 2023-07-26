from flask import render_template, Blueprint, request, flash, abort, redirect, url_for
from ..db.forms import ContactForm
from flask_login import login_required, current_user
# from routes.mail import mail
from ..db.models import Profile, Specializations, DoctorsTable, Appointment
from ..db.db import db
from datetime import datetime


pages = Blueprint(
    "pages", __name__,
    template_folder="templates",
    static_folder="static"
)


@pages.route("/")
def home():
    return render_template("home.html")


@pages.route("/appointment", methods=["GET", "POST"])
@login_required
def appointment():
    if request.method == "GET":
        specs = Specializations.query.all()
        return render_template("appointment.html", specs=specs)
    elif request.method == "POST":
        specs_id = Specializations.query.filter_by(specialization=request.form["specs"]).first()
        doctors = DoctorsTable.query.filter_by(specializations=specs_id).all()
        return render_template("appointment.html", specs=Specializations.query.all(), doctors=doctors)


@pages.route("/app_details/<int:app_id>", methods=["GET", "POST"])
@login_required
def app_details(app_id: int): #for patient to book

    # if request.method == "POST":
    #     doctor_id = 
    #     new_app = Appointment(
    #         app_date = date,
    #         app_time = time,
    #         availability = True,
    #         patient_id=current_user.id,
    #         doctor_id = doctor_id
    #         )
    # flash("Your appointment has been booked")
    appointments = Appointment.query.filter_by(app_id=app_id).all()
    return render_template('app_details.html', appointments=appointments)


@pages.route("/create_app", methods=["GET", "POST"])
@login_required
def create_app(): #for doctors
    if request.method == "POST":
        selected_date = request.form["selected_date"]
        selected_time = request.form["selected_time"]

        new_app = Appointment(
            app_date = selected_date,
            app_time = selected_time,
            availability = True,
            doctor_id = current_user._id
        )

        db.session.add(new_app)
        db.session.commit()
        flash("Appoitment slot created!")
        return render_template("create_app.html")
    return render_template("create_app.html")



@pages.route("/profile/<int:_id>", methods=["GET", "POST"])
@login_required
def profile(_id: int):
    if request.method == "GET":
        profile_data = Profile.query.filter_by(userid=_id).first()
        if not profile_data:
            abort(404)
        else:
            return render_template("profile.html", profile_data=profile_data)


@pages.route("/edit_profile/<int:_id>", methods=["GET", "POST"])
@login_required
def edit_profile(_id: int):
    profile_data = Profile.query.filter_by(userid=_id).first()
    
    if request.method == "POST":
        profile_data.name = request.form["name"]
        profile_data.surname = request.form["surname"]
        profile_data.birthdate = request.form["birthdate"]
        profile_data.telephone = request.form["telephone"]

        db.session.commit()
        return redirect(url_for(".profile.html"))
    
    return render_template("edit_profile.html", profile_data=profile_data)


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
        # else:
        #     msg = Message(form.subject.data, sender="example@example.com",
        #                   recipients=["example@example.com"])
        #     msg.body = """
        #     From: %s &lt;%s&gt;
        #     %s
        #     """ % (form.name.data, form.email.data, form.message.data)
        #     mail.send(msg)
        #     return "E-mail sent"
    elif request.method == "GET":
        return render_template("contact.html", form=form)
