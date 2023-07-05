from dataclasses import dataclass
from flask_login import UserMixin
from db import db
from datetime import datetime

@dataclass
class User(UserMixin, db.Model):
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    createdDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False, nullable=False)
    isDoctor = db.Column(db.Boolean, default=False, nullable=False)
    isPatient = db.Column(db.Boolean, default=True, nullable=False)
    isActive = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, email, password, isAdmin, isDoctor, isPatient, isActive):
        self.email = email
        self.password = password
        """
        self.isAdmin = isAdmin
        self.isDoctor = isDoctor
        self.isPatient = isPatient
        self.isActive = isActive
        """

    def get_id(self):
        return self._id


class Profile(db.Model):
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True) #db.ForeignKey('user._id')
    name = db.Column(db.String(100), unique=False)
    surname = db.Column(db.String(100), unique=False)
    birthdate = db.Column(db.DateTime, unique=False)
    email = db.Column(db.String(100), unique=True)
    telephone = db.Column(db.Integer, unique=False)
    createdDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, name, surname, birthdate, email, telephone):
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.email = email
        self.telephone = telephone
    
class DoctorsTable(db.Model):
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500), nullable=False)
    surname = db.Column(db.String(500), nullable=False)
    specialization = db.Column(db.String(500), nullable=False)

    def __init__(self, name, surname, specialization):
        self.name = name
        self.surname = surname
        self.specialization = specialization


class Specializations(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    specialization = db.Column(db.String(500), nullable=False)

    def __init__(self, specialization):
        self.specialization = specialization

