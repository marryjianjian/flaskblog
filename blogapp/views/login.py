from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..forms import LoginForm

login_and_out = Blueprint('login_and_out', __name__)


@login_and_out.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        print('login success')
        flash('login success')
        return redirect(url_for('user.index', name=form.username.data))

    return render_template('login.html', form=form)
