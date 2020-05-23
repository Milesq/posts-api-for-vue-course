from flask import Blueprint

from ..auth import auth


crud = Blueprint('crud', __name__)


@crud.route('/create', methods=['POST'])
@auth.login_required
def create_post():
    return {'data': True}
