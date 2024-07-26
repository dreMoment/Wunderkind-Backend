# app/models/parent.py
from app import db
from flask_login import UserMixin
class Parent(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(300))  
    profile_picture = db.Column(db.String(5))
    show_tutorial = db.Column(db.Boolean, nullable=False, default=True)


    def __init__(self, name, email, password_hash, profile_picture):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.profile_picture = profile_picture
        self.show_tutorial = True



