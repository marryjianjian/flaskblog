from flask import render_template, request, flash, redirect, url_for
from ..forms import LoginForm, RegisterForm
from ..models import User
from . import login_and_out


@login_and_out.route('/')
def index():

    return "Hello"


@login_and_out.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        print('login success')
        flash('login success')
        return redirect(url_for('user.index', name=form.username.data))

    return render_template('user/login.html', form=form)


@login_and_out.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        User.add_user(username=form.username.data,
                      password=form.password.data)
        flash('register success')
        return redirect(url_for('user.login'))

    return render_template('user/register.html', form=form)
