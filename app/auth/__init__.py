import os

from flask import current_app as app
from flask_httpauth import HTTPTokenAuth
import jwt

from .register import register_routes
from .login import login_routes

app.register_blueprint(register_routes, url_prefix='/users')
app.register_blueprint(login_routes, url_prefix='/users')


auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    print(token)
    return True
    # secret = os.getenv('PRIVATE_KEY')

    # try:
    #     payload = jwt.decode(token, secret, algorithms=['HS256'])

    #     db = get_db()
    #     user = payload['user']
    #     user = db.execute(f'SELECT id FROM users WHERE name="{user}"')
    #     return user.fetchone()[0]
    # except jwt.exceptions.DecodeError:
    #     pass
