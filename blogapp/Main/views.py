from flask import render_template, redirect, flash, url_for, request
from flask import current_app
from ..models import Post
from .. import db
from . import main


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.pub_date.desc()).paginate(
        page, per_page=current_app.config['POST_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/articles/<article_id>')
def article_details(article_id):
    post = Post.query.filter_by(id=article_id).first()
    post.num_of_view += 1
    db.session.commit()
    return render_template('article_details.html', post=post)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/archives')
def archives():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.pub_date.desc()).paginate(
        page, per_page=current_app.config['ARCHIVE_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    print(posts[0].pub_date.date())
    return render_template('archives.html', posts=posts, pagination=pagination)


## Error Handler Views

@main.app_errorhandler(403)
def forbidden(e):
    return render_template('error.html', error=403), 403


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=404), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error=500), 500
