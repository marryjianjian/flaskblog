from flask import Blueprint

user = Blueprint('user', __name__)
login_and_out = Blueprint('login_and_out', __name__)

from . import user, login
