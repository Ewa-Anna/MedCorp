from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class DoctorsTable(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
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

db.create_all()


@dataclass
class User:
    _id: str
    email: str
    password: str
