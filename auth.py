import sqlite3
from os import path

import bcrypt
from base64 import b64encode
from hashlib import sha256

from flask import request, make_response, Response, Blueprint

auth = Blueprint('auth', __name__)


def json_err(err: str) -> str:
    return '{"error": "%s"}' % err


@auth.route('/users/register', methods=['POST'])
def register():
    data = request.json

    if 'user' not in data or 'pass' not in data:
        return make_response(json_err('User name or password wasn\'t provided'), 400)

    user, password = data['user'], data['pass']

    if len(user) < 4 or len(password) < 6:
        return make_response(json_err('User name or password is too short'), 400)

    password = bcrypt.hashpw(
        b64encode(sha256(password.encode()).digest()),
        bcrypt.gensalt()
    )

    save_user(user, password)

    return 'hashed'


def save_user(name: str, passwd: str):
    db = get_db()
    # db.execute('INSERT INTO users VALUES ("", "")')


DB_FILE = 'posts.db'
with open('setup.sql', 'r') as f:
    DB_SETUP = ''.join(f.readlines())


def get_db():
    db = sqlite3.connect(DB_FILE)
    table = db.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users'")

    if table.fetchone()[0] != 1:
        db.executescript(DB_SETUP)

    return db
