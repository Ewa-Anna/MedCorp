from flask import render_template, Blueprint, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user

from sqlalchemy import func

from werkzeug.security import generate_password_hash

from ..db.forms import AddSpecialization, EditUser,  CreateNewUser
from ..db.models import Profile, Specializations, Appointment, User
from ..db.db import db

from ..valid import isProperMail


admin = Blueprint(
    "admin", __name__,
    template_folder="templates",
    static_folder="static"
)


@admin.route("/adminpanel")
@login_required
def admin_panel():
    return render_template("admin/adminpanel.html")


@admin.route("/adminpanel/delete_user/<int:_id>")
@login_required
def delete_user(_id: int):
    user = User.query.get_or_404(_id)
    profile = Profile.query.filter_by(userid=_id).first()

    if profile:
        db.session.delete(profile)

    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "success")
    return redirect(url_for("admin.ava_users"))


@admin.route("/adminpanel/edit_user/<int:_id>", methods=["GET", "POST"])
@login_required
def edit_user(_id: int):
    user = User.query.get_or_404(_id)
    profile = Profile.query.get_or_404(_id)
    form = EditUser(obj=user)
    form.specialization.choices = [
        (spec._id, spec.specialization) for spec in Specializations.query.all()]

    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(user)

        if user.isDoctor:
            specialization_id = form.specialization.data
            user.specs_id = specialization_id

        db.session.commit()
        flash("User data has been updated", "success")
        return redirect(url_for("admin.ava_users", _id=user._id))

    return render_template("admin/edit_user.html", form=form, user=user, profile=profile)


@admin.route("/adminpanel/ava_users", methods=["GET"])
@login_required
def ava_users():
    users = User.query.all()
    return render_template("admin/ava_users.html", users=users)


@admin.route("/adminpanel/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    form = CreateNewUser()

    if request.method == "POST":
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        isAdmin = form.isAdmin.data
        isDoctor = form.isDoctor.data
        isPatient = form.isPatient.data
        isActive = form.isActive.data

        user = User.query.filter_by(email=email).first()

        if user:
            flash("User already exists.")
            return redirect(url_for("admin.adminpanel"))

        if not isProperMail(email):
            flash("Please provide correct email address.")
            return redirect(url_for("admin.add_user"))

        if password != confirm_password:
            flash("Passwords are not matching.")
            return render_template("admin/add_user.html")

        new_user = User(email=email,
                        password=password,
                        isAdmin=isAdmin,
                        isDoctor=isDoctor,
                        isPatient=isPatient,
                        isActive=isActive)

        profile = Profile(user=new_user, email=email)

        db.session.add(new_user)
        db.session.add(profile)
        db.session.commit()

        flash("New user created successfully!", "success")
        return redirect(url_for("admin.ava_users"))
    return render_template("admin/add_user.html", form=form)


@admin.route("/adminpanel/content", methods=["GET", "POST"])
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
            return redirect(url_for("admin.content"))

    specializations = Specializations.query.all()
    appointments = Appointment.query.all()
    appointment = Appointment.query.first()

    if appointment.doctor_id:
        doctor_profile = Profile.query.filter_by(
            userid=appointment.doctor_id).first()
    else:
        doctor_profile = None

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
            return render_template("admin/content.html", doctor_profile=doctor_profile)

    return render_template("admin/content.html", form=form,
                           specializations=specializations,
                           appointments=appointments, doctor_profile=doctor_profile)


@admin.route("/adminpanel/content/delete_spec/<int:spec_id>")
@login_required
def delete_spec(spec_id):
    specialization = Specializations.query.get_or_404(spec_id)
    db.session.delete(specialization)
    db.session.commit()
    flash(
        f"The specialization '{specialization.specialization}' has been deleted!", "success")
    return redirect(url_for("admin.content"))


@admin.route("/adminpanel/analytics")
@login_required
def analytics():
    total_users = User.query.count()
    doctors_count = User.query.filter_by(isDoctor=True).count()
    appointments_count = Appointment.query.count()
    return render_template("admin/analytics.html", total_users=total_users,
                           doctors_count=doctors_count,
                           appointments_count=appointments_count)


@admin.route("/get_data", methods=["GET"])
def get_data():
    app_data = db.session.query(func.count(
        Appointment.app_id), Appointment.app_time).group_by(Appointment.app_time).all()

    timeslots = []
    app_count = []

    for count, app_time in app_data:
        timeslots.append(app_time)
        app_count.append(count)

   
    grouped_data = {}
    for i in range(len(timeslots)):
        time = timeslots[i]
        time_split = time.split(":")
        hours = int(time_split[0])
        minutes = int(time_split[1])
        interval_hours = hours + (minutes // 30) * 0.5
        interval = f"{interval_hours:.1f}"

        if interval not in grouped_data:
            grouped_data[interval] = 0
        grouped_data[interval] += app_count[i]
        grouped_data = {float(key): value for key, value in grouped_data.items()}
       
    response_data = {
        "data": {
        "timeslots": timeslots,
        "app_count": app_count
        },
        "grouped_data": grouped_data}

    return jsonify(response_data)
