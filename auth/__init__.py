from .register import register_routes
from .login import login_routes


def register(app):
    app.register_blueprint(register_routes)
    app.register_blueprint(login_routes)
