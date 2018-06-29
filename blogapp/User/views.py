from flask import render_template, request, flash, redirect, url_for
from flask import jsonify, current_app
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import LoginForm, RegisterForm, PostForm, TagForm
from ..models import User, Post, Tag
from .. import db
from . import auth, user
from datetime import datetime


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            print(user)
            login_user(user)
            flash('login success')
            return redirect(url_for('user.index'))
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
@login_required
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        User.add(username=form.username.data,
                      password=form.password.data)
        flash('register success')
        return redirect(url_for('auth.login'))

    return render_template('user/register.html', form=form)


@user.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.pub_date.desc()).paginate(
        page, per_page=current_app.config['POST_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user/index.html', posts=posts, 
        pagination=pagination, name=current_user.username)


@user.route('/addpost', methods=['GET', 'POST'])
@login_required
def add_post():
    tags = Tag.query.all()
    tags_list = [(tag.id, tag.name) for tag in tags]
    form = PostForm()
    form.tag.choices = tags_list

    if form.validate_on_submit():
        post_tag = tags_list[int(form.tag.data)-1][1]
        tag = Tag.query.filter_by(name=post_tag).first()
        post = Post(title=form.title.data, content=form.content.data, tag=tag)
        Post.add(post=post)
        flash('add post success')
        return redirect(url_for('user.index'))

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


@user.route('/deletepost')
@login_required
def delete_post():
    try:
        post_id = request.args.get('post_id', type=int)
    except:
        flash('delete post failed')

    Post.delete(id=post_id)
    flash('delete post secess')
    return redirect(url_for('user.index'))


@user.route('/editpost', methods=['GET', 'POST'])
@login_required
def edit_post():
    try:
        post_id = request.args.get('post_id', type=int)
    except:
        flash('edit post failed')

    post = Post.query.filter_by(id=post_id).first()
    tags = Tag.query.all()
    tags_list = [(tag.id, tag.name) for tag in tags]
    form = PostForm()
    form.tag.choices = tags_list

    if form.validate_on_submit():
        post_tag = tags_list[int(form.tag.data)-1][1]
        tag = Tag.query.filter_by(name=post_tag).first()
        post.title = form.title.data
        post.content = form.content.data
        post.tag = tag
        post.up_date = datetime.utcnow()
        db.session.commit()
        flash('post update sucess')
        return redirect(url_for('user.index'))

    form.title.data = post.title
    form.content.data = post.content
    form.tag.data = post.tag_id - 1
    return render_template('user/addpost.html', form=form)


@user.route('/todict', methods=['GET', 'POST'])
@login_required
def to_dict():
    try:
        post_id = request.args.get('post_id')
    except:
        flash('to dict failed')

    post = Post.query.filter_by(id=post_id).first()
    post_dict = post.to_dict()
    return str(post_dict)

