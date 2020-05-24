from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_only = ('name',)

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(16), unique=True, nullable=False)

    passwd = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'


class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    serialize_rules = ('-id', '-author_id')

    id = db.Column(db.Integer, primary_key=True)

    uuid = db.Column(db.String(36), unique=True, nullable=False)

    title = db.Column(db.String(76), nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                          nullable=False)
    author = db.relationship(
        'User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Post {self.title}>'
