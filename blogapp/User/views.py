from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from ..forms import LoginForm, RegisterForm, PostForm
from ..models import User, Post
from . import auth, user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    try:
        print(User.query.all())
    except:
        print('Error')

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            print(user)
            login_user(user)
            flash('login success')
            return redirect(url_for('auth.index',
                                    name=form.username.data))
        else:
            flash('Wrong!', 'danger')

    return render_template('user/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout success')
    return redirect(url_for('auth.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        User.add(username=form.username.data,
                      password=form.password.data)
        flash('register success')
        return redirect(url_for('auth.login'))

    return render_template('user/register.html', form=form)


@user.route('/<name>')
def index(name):
    print('Hello %r' % name)
    return render_template('user/index.html', name=name)


@user.route('/addpost')
def add_post():
    form = PostForm()
    pass
