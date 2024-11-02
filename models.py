from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

#from app import app

db = SQLAlchemy()

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False)

    #def check_password(self, password):
     #   return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Предустановленные роли
def create_roles():
    db.create_all()
    roles = ['User', 'Admin', 'Manager']
    for role in roles:
        if not UserRole.query.filter_by(name=role).first():
            new_role = UserRole(name=role)
            db.session.add(new_role)
    db.session.commit()

