from flask import render_template, redirect, flash, url_for
from ..models import Post
from . import main

@main.route('/')
def index():
    print('HHH')
    try:
        posts = Post.query.all()
    except:
        print('Query Fail')

    return render_template('index.html', posts=posts)
