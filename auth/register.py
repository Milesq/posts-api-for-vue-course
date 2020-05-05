import bcrypt

from sqlescapy import sqlescape
from flask import request, make_response, Response, Blueprint

from db_utils import get_db

register_routes = Blueprint('register', __name__)


class RegisterException(BaseException):
    pass


@register_routes.route('/users/register', methods=['POST'])
def register():
    data = request.json

    if 'user' not in data or 'pass' not in data:
        return make_response({"error": 'User name or password wasn\'t provided'}, 400)

    user, password = data['user'], data['pass']

    if len(user) < 4 or len(password) < 6:
        return make_response({"error": 'User name or password is too short'}, 400)

    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(14)).decode()

    try:
        save_user(user, password)
    except RegisterException as err:
        return {"error": str(err)}

    return {"token": "secret"}


def save_user(name: str, passwd: str):
    name = sqlescape(name)
    db = get_db()
    user = db.execute(f'SELECT name FROM users WHERE name="{name}"')

    if user.fetchone() == None:
        db.execute(f'INSERT INTO users VALUES ("{name}", "{passwd}")')
        db.commit()
        db.close()
    else:
        raise RegisterException('User already exists')
