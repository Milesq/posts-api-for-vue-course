import bcrypt

from sqlescapy import sqlescape
from flask import request, make_response, Response, Blueprint

from ..models import db, User
from ..limiter import limiter

register_routes = Blueprint('register', __name__)


class RegisterException(BaseException):
    pass


@register_routes.route('/register', methods=['POST'])
@limiter.limit('1/minute')
def register():
    data = request.json

    if 'user' not in data or 'pass' not in data:
        return make_response({"error":
                              'User name or password wasn\'t provided'}, 400)

    user, password = data['user'], data['pass']

    if len(user) < 4 or len(password) < 6:
        return make_response({"error":
                              'User name or password is too short'}, 400)

    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(14)).decode()

    try:
        save_user(user, password)
    except RegisterException as err:
        return {"error": str(err)}

    return {"data": True}


def save_user(name: str, passwd: str):
    new_user = User(name=sqlescape(name), passwd=passwd)
    user = User.query.filter(User.name == new_user.name).first()

    if user is None:
        db.session.add(new_user)
        db.session.commit()
    else:
        raise RegisterException('User already exists')
