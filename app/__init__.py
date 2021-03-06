from flask import Flask
from flask_cors import CORS

from config import config
from .models import db
from .limiter import limiter

app = Flask(__name__)
CORS(app)
config(app)
db.init_app(app)

app.config["RATELIMIT_DEFAULT"] = '30/minute'

limiter.init_app(app)

with app.app_context():
    db.create_all()
    from . import routes
