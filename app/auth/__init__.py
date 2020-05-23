import os

from flask import current_app as app
from flask_httpauth import HTTPTokenAuth
import jwt

from .register import register_routes
from .login import login_routes
from ..models import db, User

app.register_blueprint(register_routes, url_prefix='/users')
app.register_blueprint(login_routes, url_prefix='/users')


auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    secret = os.getenv('PRIVATE_KEY')

    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])

        user = payload['user']
        return User.query.filter_by(name=user).first()
    except jwt.exceptions.DecodeError:
        pass
