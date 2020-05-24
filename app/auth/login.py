import os

from flask import request, Blueprint, make_response
from sqlescapy import sqlescape
from bcrypt import checkpw
import jwt

from ..models import db, User
from util import have

login_routes = Blueprint('login', __name__)


@login_routes.route('/login', methods=['POST'])
def login():
    data = request.json

    if not have(data, ['user', 'pass']):
        return make_response({"error":
                              'User name or password wasn\'t provided'}, 400)

    user, password = sqlescape(data['user']), data['pass'].encode()

    user: User = User.query.filter_by(name=user).first()

    if user is None:
        return make_response({"error": "User doesn't exists"}, 401)

    if not checkpw(password, user.passwd.encode('utf-8')):
        return make_response({"error": "Password is incorrect"}, 401)

    secret = os.getenv('PRIVATE_KEY')

    if secret is None:
        print('Private key is not set!!!')
        return make_response({"error": "Private key is not set"}, 500)

    encoded_jwt = jwt.encode({'user': user.name}, secret, algorithm='HS256')

    return {"token": encoded_jwt.decode()}
