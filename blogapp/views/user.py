from flask import Blueprint, render_template


user = Blueprint('user', __name__, url_prefix='user/<name>')


# @user.route('/<name>')
# def show_username(name):
#     return render_template('user/index.html', name=name)


@user.route('/')
def index(name):
    print('Hello %r' % name)
    return render_template('user/index.html', name=name)
