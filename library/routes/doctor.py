from flask import render_template, Blueprint, request, flash,  redirect, url_for
from flask_login import login_required, current_user

from ..db.forms import EditRecommendation
from ..db.models import Appointment
from ..db.db import db


doctor = Blueprint(
    "doctor", __name__,
    template_folder="templates",
    static_folder="static"
)


@doctor.route("/create_app", methods=["GET", "POST"])
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
        return render_template("doctor/create_app.html")
    return render_template("doctor/create_app.html")


@doctor.route("/edit_recommendation/<int:app_id>", methods=["GET", "POST"])
@login_required
def edit_recommendation(app_id: int):
    appointment = Appointment.query.get(app_id)
    form = EditRecommendation(obj=appointment)

    if appointment.doctor_id != current_user._id:
        flash("You are not authorized. Please log in as a doctor.", "danger")
    
    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(appointment)
        db.session.commit()
        flash("Recommendation updated successfully.", "success")
        return redirect(url_for("pages.app_details", app_id=app_id))
    
    return render_template("doctor/edit_recommendation.html", form=form, appointment=appointment)


@doctor.route("/delete_recommendations/<int:app_id>", methods=["GET", "POST"])
@login_required
def delete_recommendations(app_id: int):
    if request.method == "POST":
        appointment = Appointment.query.get_or_404(app_id)
        
        if appointment.doctor_id != current_user._id:
            flash("You are not authorized. Please log in as a doctor.", "danger")
        else:
            appointment.recommendations = None
            db.session.commit()
            flash("Recommendations deleted successfully.", "success")

        return redirect(url_for("pages.app_details", app_id=app_id))
    else:
        return redirect(url_for("pages.app_details", app_id=app_id))
    
