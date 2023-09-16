from library.db.models import User, Appointment
from library.db.db import db


def test_doctor_appointment(app):
    test_doctor = User(email="doctor@doctor.com", password="123", isAdmin=False,
                       isDoctor=True, isPatient=True, isActive=True)
    db.session.add(test_doctor)
    db.session.commit()

    test_appointment_slot = Appointment(
        app_date="2023-08-22", app_time="12:00", availability=True, doctor_id=test_doctor._id)
    db.session.add(test_appointment_slot)
    db.session.commit()

    assert test_doctor._id is not None
    assert test_appointment_slot.app_id is not None


def test_patient_appointment(app):
    test_patient = User(email="patient@patient.com", password="123",
                        isAdmin=False, isDoctor=False, isPatient=True, isActive=True)
    db.session.add(test_patient)
    db.session.commit()

    available_appointment = Appointment.query.filter_by(availability=True).first()

    if available_appointment:
        available_appointment.availability = False
        available_appointment.patient_id = test_patient._id
        db.session.commit()

        assert available_appointment.availability is False
        assert available_appointment.patient_id == test_patient._id
    else:
        print("No available appointments found.")
