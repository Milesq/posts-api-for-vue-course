from flask import Flask, Blueprint
from dotenv import load_dotenv

from auth import register as auth_blueprint, auth
from posts import register as posts_blueprint

load_dotenv()

app = Flask(__name__)
auth_blueprint(app)
posts_blueprint(app)
