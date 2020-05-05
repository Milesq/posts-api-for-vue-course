import os

from flask import request, Blueprint, make_response
from sqlescapy import sqlescape
from bcrypt import checkpw
import jwt

from db_utils import get_db

login_routes = Blueprint('login', __name__)


@login_routes.route('/users/login', methods=['POST'])
def login():
    data = request.json

    if 'user' not in data or 'pass' not in data:
        return make_response({"error": 'User name or password wasn\'t provided'}, 400)

    user, password = sqlescape(data['user']), data['pass'].encode()

    db = get_db()
    pass_hash = db.execute(
        f'SELECT pass FROM users WHERE name="{user}"').fetchone()

    if pass_hash == None:
        return make_response({"error": "User doesn't exists"}, 401)

    if not checkpw(password, pass_hash[0].encode('utf-8')):
        return make_response({"error": "Password is incorrect"}, 401)

    secret = os.getenv('PRIVATE_KEY')
    encoded_jwt = jwt.encode({'user': user}, secret, algorithm='HS256')

    return {"token": encoded_jwt.decode()}
