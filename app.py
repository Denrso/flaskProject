from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes import *



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание всех таблиц
    app.run(debug=True)
