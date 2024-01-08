from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_pagedown import PageDown


db = SQLAlchemy()
bcrypt_app = Bcrypt()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__,
                instance_relative_config=True,
                static_url_path='/old/static')

    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    db.init_app(app)
    bcrypt_app.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)

    from .User import user, auth
    from .Main import main

    app.register_blueprint(user, url_prefix='/old/user')
    app.register_blueprint(auth, url_prefix='/old')
    app.register_blueprint(main, url_prefix='/old')

    # if db.init_app called after the blueprint register ,
    # codes below is needed
    # with app.app_context():
    #     db.create_all()

    return app
