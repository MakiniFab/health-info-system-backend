from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Association table for the many-to-many relationship between Clients and Programs
client_program = db.Table('client_program',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id')),
    db.Column('program_id', db.Integer, db.ForeignKey('program.id'))
)

# User model for authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)  # Username must be unique
    password_hash = db.Column(db.String(200))  # Hashed password for security

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Client model to store client information
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    programs = db.relationship('Program', secondary=client_program, backref='clients')
    outcomes = db.relationship('ProgramOutcome', backref='client', lazy=True)

# Program model to define different programs
class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    outcomes = db.relationship('ProgramOutcome', backref='program', lazy=True)

# ProgramOutcome model to track client progress in programs
class ProgramOutcome(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    outcome = db.Column(db.String(100))
    notes = db.Column(db.Text)

# ActivityLog model to log doctor actions (e.g., client registration, program enrollment)
class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_username = db.Column(db.String(80))
    action = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
