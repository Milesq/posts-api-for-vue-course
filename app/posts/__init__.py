from flask import current_app as app

from .crud_post import crud

app.register_blueprint(crud, url_prefix='/posts')
