from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(16), unique=True, nullable=False)

    passwd = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)

    uuid = db.Column(db.String(36), unique=True, nullable=False)

    author = db.Column(db.Integer, nullable=False)

    title = db.Column(db.String(76), nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
