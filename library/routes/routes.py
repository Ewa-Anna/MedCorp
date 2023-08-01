from flask import render_template, Blueprint, request, flash, abort, redirect, url_for
from ..db.forms import ContactForm, EditProfile, AddSpecialization, EditUser
from flask_login import login_required, current_user
from .mail import mail
from flask_mail import Message
from ..db.models import Profile, Specializations, DoctorsTable, Appointment, User
from ..db.db import db
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


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
    # if request.method == "GET":
    #     specs = Specializations.query.all()
    #     return render_template("appointment.html", specs=specs)
    # elif request.method == "POST":
    #     specs_id = Specializations.query.filter_by(specialization=request.form["specs"]).first()
    #     doctors = DoctorsTable.query.filter_by(specializations=specs_id).all()
    # return render_template("appointment.html", specs=Specializations.query.all(), doctors=doctors)

    appointment = Appointment.query.filter_by(availability=True).all()
    return render_template("appointment.html", appointment=appointment)


@pages.route("/app_details/<int:app_id>", methods=["GET", "POST"])
@login_required
def app_details(app_id: int):  # for patient to book
    appointments = Appointment.query.filter_by(app_id=app_id).all()
    if request.method == "POST":
        if appointment.availability:
            appointment.availability = False
            appointment.patient_id = current_user._id
            db.session.commit()
            flash("Appointment booked successfully!", "success")
            return redirect(url_for("pages.app_details", app_id=app_id))
        else:
            flash("This appintment is no longer available.")

    return render_template('app_details.html', appointments=appointments)


@pages.route("/create_app", methods=["GET", "POST"])
@login_required
def create_app():  # for doctors to create
    if request.method == "POST":
        selected_date = request.form["selected_date"]
        selected_time = request.form["selected_time"]

        new_app = Appointment(
            app_date=selected_date,
            app_time=selected_time,
            availability=True,
            doctor_id=current_user._id
        )

        db.session.add(new_app)
        db.session.commit()
        flash("Appointment slot created!")
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
    form = EditProfile(obj=profile_data)

    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(profile_data)
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("pages.profile", _id=_id))

    return render_template("edit_profile.html", profile_data=profile_data, form=form)


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
            msg = Message(form.subject.data, sender=EMAIL,
                          recipients=[EMAIL])
            msg.body = """
            From: %s &lt;%s&gt;
            %s
            """ % (form.name.data, form.email.data, form.body.data)
            mail.send(msg)
            return "E-mail sent"
    elif request.method == "GET":
        return render_template("contact.html", form=form)


@pages.route("/adminpanel")
@login_required
def admin_panel():
    return render_template("adminpanel.html")


@pages.route("/adminpanel/delete_user/<int:_id>")
@login_required
def delete_user(_id: int):
    user = User.query.get_or_404(_id)
    profile = Profile.query.filter_by(userid=_id).first()
    
    if profile:
        db.session.delete(profile)

    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "success")
    return redirect(url_for("pages.ava_users"))


@pages.route("/adminpanel/edit_user/<int:_id>", methods=["GET", "POST"])
@login_required
def edit_user(_id: int):
    user = User.query.get_or_404(_id)
    form = EditUser(obj=user)

    if request.method == "POST" and form.validate_on_submit():
        user.email = form.email.data
        user.isAdmin = form.isAdmin.data
        user.isDoctor = form.isDoctor.data
        user.isPatient = form.isPatient.data
        user.isActive = form.isActive.data
  
        db.session.commit()
        flash("User data has been updated", "success")
        return redirect(url_for("pages.ava_users", _id=_id))

    return render_template("edit_user.html", form=form, user=user)


@pages.route("/adminpanel/ava_users", methods=["GET"])
@login_required
def ava_users():
    users = User.query.all()
    return render_template("ava_users.html", users=users)


@pages.route("/adminpanel/content", methods=["GET", "POST"])
@login_required
def content():
    form = AddSpecialization()

    if form.validate_on_submit():
        specialization = form.specialization.data.strip()
        existing_specialization = Specializations.query.filter_by(
            specialization=specialization).first()

        if existing_specialization:
            flash(
                f"The specialization '{specialization}' already exists!", "danger")
        else:
            new_spec = Specializations(specialization=form.specialization.data)
            db.session.add(new_spec)
            db.session.commit()
            flash(
                f"The specialization '{specialization}' has been added!", "success")
            return redirect(url_for("pages.content"))

    specializations = Specializations.query.all()
    return render_template("content.html", form=form, specializations=specializations)


@pages.route("/adminpanel/content/delete_spec/<int:spec_id>")
@login_required
def delete_spec(spec_id):
    specialization = Specializations.query.get_or_404(spec_id)
    db.session.delete(specialization)
    db.session.commit()
    flash(
        f"The specialization '{specialization.specialization}' has been deleted!", "success")
    return redirect(url_for("pages.content"))


@pages.route("/adminpanel/analytics")
@login_required
def analytics():
    total_users = User.query.count()
    doctors_count = User.query.filter_by(isDoctor=True).count()
    appointments_count = Appointment.query.count()
    return render_template("analytics.html", total_users=total_users, doctors_count=doctors_count, appointments_count=appointments_count)
