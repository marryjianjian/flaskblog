from flask import Blueprint

user = Blueprint('user', __name__)
auth = Blueprint('auth', __name__)

from . import user, login
