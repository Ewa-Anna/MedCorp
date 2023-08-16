from flask import render_template, Blueprint, request, flash, abort, redirect, url_for
from flask_login import login_required, current_user
from flask_mail import Message

from ..db.forms import ContactForm, EditProfile, BookApp
from ..db.models import Profile, Specializations, Appointment, User
from ..db.db import db

from .mail import mail

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


@pages.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        booked_app = []
        appointment = []

        if current_user.is_authenticated:
            if current_user.isDoctor:
                appointment = Appointment.query.filter_by(
                    doctor_id=current_user._id).all()

            elif current_user.isPatient:
                booked_app = Appointment.query.filter_by(
                    patient_id=current_user._id).all()

        doctor_profiles = {}
        for app in appointment:
            doctor_profile = Profile.query.filter_by(
                userid=app.doctor_id).first()
            doctor_profiles[app.doctor_id] = doctor_profile

        if current_user.is_authenticated:
            display = Appointment.query.filter_by(
                patient_id=current_user._id).all()

            display_doctor = []
            for appointment in display:
                if appointment.doctor_id:
                    doctor_profile = Profile.query.filter_by(
                        userid=appointment.doctor_id).first()
                    display_doctor.append(doctor_profile)
                else:
                    display_doctor.append(None)

                return render_template("main/home.html", booked_app=booked_app, appointment=appointment, doctor_profiles=doctor_profiles, doctor_profile=doctor_profile)

        else:
            display = []
            display_doctor = []

        return render_template("main/home.html", booked_app=booked_app, appointment=appointment, doctor_profiles=doctor_profiles)

    return render_template("main/home.html")


@pages.route("/appointment", methods=["GET", "POST"])
@login_required
def appointment():
    if request.method == "GET":
        specs = Specializations.query.all()
        return render_template("main/appointment.html", specs=specs)

    elif request.method == "POST":
        selected_specialization = request.form.get("specs")
        specs_id = Specializations.query.filter_by(
            specialization=selected_specialization).first()

        if specs_id:
            appointments = Appointment.query.join(User, Appointment.doctor_id == User._id).filter(
                User.specs_id == specs_id._id, Appointment.availability == True).all()
        else:
            appointments = []

        return render_template("main/appointment.html", specs=Specializations.query.all(), appointment=appointments, selected_specialization=selected_specialization)


@pages.route("/app_details/<int:app_id>", methods=["GET", "POST"])
@login_required
def app_details(app_id: int):  # for patient to book
    appointment = Appointment.query.filter_by(app_id=app_id).first()
    form = BookApp()

    if not appointment:
        flash("Appointment not found.", "danger")
        return redirect(url_for("pages.appointment"))

    if request.method == "POST":
        if appointment.availability:
            appointment.availability = False
            appointment.patient_id = current_user._id
            db.session.commit()
            flash("Appointment booked successfully!", "success")
            return redirect(url_for("pages.app_details", app_id=app_id))

        appointment = Appointment.query.get_or_404(app_id)

        if appointment.doctor_id != current_user._id:
            flash("You are not authorized to submit recommendations.", "danger")
            return redirect(url_for("pages.app_details", app_id=app_id))

        recommendations = request.form.get("recommendations")
        appointment.recommendations = recommendations
        db.session.commit()

        flash("Recommendations submitted successfully!", "success")
        return redirect(url_for("pages.app_details", app_id=app_id, appointment=appointment))

    if appointment.doctor_id:
        doctor_profile = Profile.query.filter_by(
            userid=appointment.doctor_id).first()
        user = User.query.get(appointment.doctor_id)
        if user:
            specialization = Specializations.query.get(user.specs_id)
        else:
            specialization = None
    else:
        doctor_profile = None

    return render_template('main/app_details.html', appointment=appointment, form=form, doctor_profile=doctor_profile, specialization=specialization)


@pages.route("/profile/<int:_id>", methods=["GET", "POST"])
@login_required
def profile(_id: int):
    if request.method == "GET":
        profile_data = Profile.query.filter_by(userid=_id).first()

        if not profile_data:
            abort(404)

        return render_template("user/profile.html", profile_data=profile_data)


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

    return render_template("user/edit_profile.html", profile_data=profile_data, form=form)


@pages.route("/about")
def about():
    return render_template("main/about.html")


@pages.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if request.method == "POST":
        if form.validate() == False:
            flash("All fields are required.")
            return render_template("main/contact.html", form=form)
        else:
            msg = Message(form.subject.data, sender=EMAIL,
                          recipients=[EMAIL])
            msg.body = """
            From: %s &lt;%s&gt;
            %s
            """ % (form.name.data, form.email.data, form.body.data)
            mail.send(msg)
            return render_template("main/contact.html", success=True)
    elif request.method == "GET":
        return render_template("main/contact.html", form=form)


@pages.route("/deleteapp/<int:app_id>")
@login_required
def delete_app(app_id):
    appointment = Appointment.query.get_or_404(app_id)
    db.session.delete(appointment)
    db.session.commit()
    flash("Appointment deleted successfully.", "success")
    return redirect(request.referrer)  # redirects to current page


@pages.route("/deleteapp2/<int:app_id>")
@login_required
def delete_app_patient(app_id):
    appointment = Appointment.query.get_or_404(app_id)
    if appointment.patient_id == current_user._id:
        appointment.patient_id = None
        appointment.availability = True
        db.session.commit()
    flash("Appointment deleted successfully.", "success")
    return redirect(request.referrer)

