from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from ..forms import LoginForm, RegisterForm, PostForm, TagForm
from ..models import User, Post, Tag
from . import auth, user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # try:
    #     print(User.query.all())
    # except:
    #     print('Error')

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            print(user)
            login_user(user)
            flash('login success')
            return redirect(url_for('user.add_post'))
        else:
            flash('Wrong!', 'danger')

    return render_template('user/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout success')
    return redirect(url_for('main.index'))


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


@user.route('/addpost', methods=['GET', 'POST'])
@login_required
def add_post():
    tags = Tag.query.all()
    form = PostForm()

    if form.validate_on_submit():
        print(form.tag.data)
        return 'HH'
        tag = Tag.query.filter_by(name=form.tag.data).first()
        post = Post(title=form.title.data, content=form.content.data, tag=tag)
        Post.add(post=post)
        flash('add post success')
        return render_template('user/addpost.html', form=PostForm(), tags=tags)

    form.tag.choices = [(tag.id, tag.name) for tag in tags]
    return render_template('user/addpost.html', form=form, tags=tags)


@user.route('/addtag', methods=['GET', 'POST'])
@login_required
def add_tag():
    form = TagForm()

    if form.validate_on_submit():
        if Tag.query.filter_by(name=form.tag.data).first() is None:
            tag = Tag(name=form.tag.data)
            Tag.add(tag=tag)
            flash('add tag sucess')
        else:
            flash('The tag "%r" already exists' % form.tag.data)

        return render_template('user/addtag.html', form=TagForm())

    return render_template('user/addtag.html', form=form)
