from flask import Flask
from .crud_post import crud


def register(app: Flask):
    app.register_blueprint(crud, url_prefix='/posts')
