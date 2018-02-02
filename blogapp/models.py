from . import db, bcrypt_app, login_manager
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'),
                            nullable=False)

    tag = db.relationship('Tag',
                               backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post> %r' % self.title

    @staticmethod
    def add(post=None, title=None, content=None, tag=None):
        if post is None:
            post = Post(title=title, content=content, tag=tag)
        try:
            db.session.add(post)
            db.session.commit()
        except:
            print('Fail')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Tag %r>' % self.name

    @staticmethod
    def add(tag=None, name=name):
        if tag is None:
            tag = Tag(name=name)
        try:
            db.session.add(tag)
            db.session.commit()
        except:
            print('Fail')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self.password_hash = bcrypt_app.generate_password_hash(plaintext)

    def verify_password(self, password_input):
        return bcrypt_app.check_password_hash(self.password_hash,
                                              password_input)

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def add(user=None, username=None, password=None):
        if user is None:
            user = User(username=username, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            print('success')
        except:
            # db.session.callback()
            print('Fail')
            pass


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
