from flask import Flask, Blueprint

from auth import register as auth_blueprint
from posts import register as posts_blueprint

app = Flask(__name__)
auth_blueprint(app)
posts_blueprint(app)
