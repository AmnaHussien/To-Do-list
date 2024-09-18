from website import db
from flask_login import UserMixin
from datetime import datetime

#designing data model
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.Integer, unique = True, nullable = False)
    tasks = db.relationship('Task')
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(60))
    due_date = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
