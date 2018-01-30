from . import db, bcrypt_app, login_manager
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property


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


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Tag %r>' % self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    _password = db.Column(db.String(128), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt_app.generate_password_hash(plaintext)

    def verify_password(self, password_input):
        return bcrypt_app.check_password_hash(self._password, password_input)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def add_user(username, passowrd):
        user = User(username=username, password=password)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.callback()


@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User,id==userid).first()
