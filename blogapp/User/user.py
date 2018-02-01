from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, login_required
from ..models import Post
from ..forms import PostForm
from . import user


@user.route('/<name>')
def index(name):
    print('Hello %r' % name)
    return render_template('user/index.html', name=name)


@user.route('/addpost')
def add_post():
    form = PostForm()
