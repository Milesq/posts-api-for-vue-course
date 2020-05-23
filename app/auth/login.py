from flask import Blueprint


login_routes = Blueprint('login', __name__)


@login_routes.route('/login', methods=['POST'])
def login():
    return "ok"
