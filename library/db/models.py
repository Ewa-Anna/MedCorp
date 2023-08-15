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
    specs_id = db.Column(db.Integer, db.ForeignKey("specializations._id"))
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

    specializations = db.relationship("Specializations", uselist=False, cascade="delete")

class Profile(db.Model):
    __tablename__ = 'profile'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False)
    surname = db.Column(db.String(100), unique=False)
    birthdate = db.Column(db.DateTime, unique=False)
    email = db.Column(db.String(100), unique=True)
    telephone = db.Column(db.Integer, unique=False)
    insurance = db.Column(db.Boolean)
    userid = db.Column(db.Integer, db.ForeignKey("user._id"), nullable=False, unique=True)
    createdDate = db.Column(db.DateTime,
                            default=datetime.utcnow, nullable=False)

    user = db.relationship("User", uselist=False, cascade="delete")

    def get_birthdate(self):
        if self.birthdate:
            return self.birthdate.strftime('%e %B %Y')
        return ''


class Appointment(db.Model):
    __tablename__ = 'appointment'

    app_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_date = db.Column(db.Text, nullable=False)
    app_time = db.Column(db.Text, nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("profile._id"))
    doctor_id = db.Column(db.Integer)
    createdDate = db.Column(db.DateTime,
                            default=datetime.utcnow, nullable=False)
    recommendations = db.Column(db.Text)
    
    profile = db.relationship("Profile", uselist=False)

class Specializations(db.Model):
    __tablename__ = 'specializations'

    _id = db.Column(db.Integer, primary_key=True)
    specialization = db.Column(db.String(500), nullable=False)
