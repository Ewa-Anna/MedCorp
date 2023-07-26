from dataclasses import dataclass
from flask_login import UserMixin
from .db import db
from datetime import datetime


@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    createdDate = db.Column(db.DateTime,
                            default=datetime.utcnow, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False, nullable=False)
    isDoctor = db.Column(db.Boolean, default=False, nullable=False)
    isPatient = db.Column(db.Boolean, default=True, nullable=False)
    isActive = db.Column(db.Boolean, default=True, nullable=False)


    def __init__(self, email, password, isAdmin,
                 isDoctor, isPatient, isActive):
        self.email = email
        self.password = password
        self.isAdmin = isAdmin
        self.isDoctor = isDoctor
        self.isPatient = isPatient
        self.isActive = isActive


    def get_id(self):
        return self._id


class Profile(db.Model):
    __tablename__ = 'profile'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False)
    surname = db.Column(db.String(100), unique=False)
    birthdate = db.Column(db.DateTime, unique=False)
    email = db.Column(db.String(100), unique=True)
    telephone = db.Column(db.Integer, unique=False)
    insurance = db.Column(db.Boolean, unique=True)
    userid = db.Column(db.Integer, db.ForeignKey("user._id"), nullable=False)
    createdDate = db.Column(db.DateTime,
                            default=datetime.utcnow, nullable=False)

    user = db.relationship("User", uselist=False, cascade="delete")


class Appointment(db.Model):
    __tablename__ = 'appointment'

    app_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_date = db.Column(db.Text, nullable=False)
    app_time = db.Column(db.Text, nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("user._id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctorstable._id"), nullable=False)
    createdDate = db.Column(db.DateTime,
                            default=datetime.utcnow, nullable=False)
    
    user = db.relationship("User", uselist=False, cascade="delete")
    doctorstable = db.relationship("DoctorsTable", uselist=False, cascade="delete")

class DoctorsTable(db.Model):
    __tablename__ = 'doctorstable'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500), nullable=False)
    surname = db.Column(db.String(500), nullable=False)
    specs_id = db.Column(db.Integer, db.ForeignKey("specializations._id"), nullable=False)

    specializations = db.relationship("Specializations", uselist=False, cascade="delete")

class Specializations(db.Model):
    __tablename__ = 'specializations'

    _id = db.Column(db.Integer, primary_key=True)
    specialization = db.Column(db.String(500), nullable=False)
