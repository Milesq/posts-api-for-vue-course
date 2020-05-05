import os

from flask_httpauth import HTTPTokenAuth
import jwt

from .register import register_routes
from .login import login_routes


def register(app):
    app.register_blueprint(register_routes)
    app.register_blueprint(login_routes)


auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    secret = os.getenv('PRIVATE_KEY')

    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])

        return payload['user']
    except jwt.exceptions.DecodeError:
        pass
