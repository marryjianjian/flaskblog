from flask import render_template
from . import user


@user.route('/<name>')
def index(name):
    print('Hello %r' % name)
    return render_template('user/index.html', name=name)
