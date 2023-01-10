from leadest import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from io import BytesIO
from flask import Flask

@login_manager.user_loader
def load_user(user_id):
    print(User.query.get(user_id))
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), nullable=False)
    id_m = db.Column(db.Integer, nullable=False)
    date_start = db.Column(db.Date, nullable=True)
    birthdate = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128))
    files = db.relationship('LeadsFile', backref='branchmanager', lazy='dynamic')
    owner = db.relationship('Branch', backref='branchmanager', uselist=False)

    def __init__(self, role, username, name, id_m, email, phone, gender, password):
        self.role = role
        self.username = username
        self.name = name
        self.id_m = id_m
        self.email = email
        self.phone = phone
        self.gender = gender
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"UserName is: {self.username}"


class LeadsFile(db.Model):
    __tablename__ = 'files'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    counter = db.Column(db.Integer)

    def __init__(self, filename, data, user_id, date, counter):
        self.filename = filename
        self.data = data
        self.user_id = user_id
        self.date = date
        self.counter = counter

    def __repr__(self):
        return f"File details: {self.filename} --- ID bm: {self.id}"


class Branch(db.Model):
    __tablename__ = 'branches'
    id_b = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    workers = db.relationship('Worker', backref='working', lazy='dynamic')

    def __init__(self, company_name, address, city, manager_id):
        self.company_name = company_name
        self.address = address
        self.city = city
        self.manager_id = manager_id

    def __repr__(self):
        return str(self.id_b)


class Worker(db.Model):
    __tablename__ = 'workers'
    id_w = db.Column(db.Integer, primary_key=True)
    year_birth = db.Column(db.String(64), nullable=False)
    year_start = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    main_specialty = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(64), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id_b'))

    def __init__(self, year_birth, year_start, name, main_specialty, gender, branch_id):
        self.year_birth = year_birth
        self.year_start = year_start
        self.name = name
        self.main_specialty = main_specialty
        self.gender = gender
        self.branch_id = branch_id

    def __repr__(self):
        return f"Worker details: {self.id_w} --- Wokrer name: {self.name} "
