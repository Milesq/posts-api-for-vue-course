from flask import Flask, Blueprint

from auth import register

app = Flask(__name__)
register(app)
