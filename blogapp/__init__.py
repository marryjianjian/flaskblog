from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy()
bcrypt_app = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    db.init_app(app)
    bcrypt_app.init_app(app)
    login_manager.init_app(app)

    from .User import user, auth

    app.register_blueprint(user, url_prefix='/user/<name>')
    app.register_blueprint(auth)

    # if db.init_app called after the blueprint register ,
    # codes below is needed
    # with app.app_context():
    #     db.create_all()

    return app
