from flask import request, Blueprint

login_routes = Blueprint('login', __name__)


@login_routes.route('/users/login', methods=['POST'])
def login():
    return {"token": "secret", "name": request.json}
