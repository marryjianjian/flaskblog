from flask import Blueprint, render_template


user = Blueprint('user', __name__)


@user.route('/<name>')
def show_username(name):
    return render_template('user/index.html', name=name)


@user.route('/')
def index():
    return "This is index"
