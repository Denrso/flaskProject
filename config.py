import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/flask_shop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False