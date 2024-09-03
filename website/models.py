from . import db
from flask_login import UserMixin
from datetime import datetime

#designing data model
class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username= db.Column(db.String(50))
    email = db.Column(db.String(40), unique = True, nullable = False)
    password = db.Column(db.Integer, unique = True, nullable = False)
    tasks = db.relationship('task')
class task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(60))
    #content => title
    #description = db.column(db.String(60))
    is_complete = db.Column(db.Boolean)
    due_date = db.Column(db.DateTime, default= datetime.utcnow)
    deadline = db.Column(db.DateTime, default = datetime.date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    def __repr__(self):
        return f"Task{sef.id}"
