from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .views.user import user


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    app.register_blueprint(user, url_prefix='/user')

    db = SQLAlchemy()
    db.init_app(app)
    bcrypt_app = Bcrypt()
    bcrypt_app.init_app(app)

    return app
