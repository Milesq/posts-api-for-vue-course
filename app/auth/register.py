from flask import Blueprint


register_routes = Blueprint('register', __name__)


@register_routes.route('/register', methods=['POST'])
def register():
    return "ok"
