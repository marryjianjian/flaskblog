from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .views.user import user
from .views.login import login_and_out

db = SQLAlchemy()
bcrypt_app = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    app.register_blueprint(user, url_prefix='/user/<name>')
    app.register_blueprint(login_and_out)

    db.init_app(app)
    bcrypt_app.init_app(app)
    login_manager.init_app(app)

    return app
