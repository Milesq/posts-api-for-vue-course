from os import path

from flask import Flask

basedir = path.abspath(path.dirname(__file__))


def config(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + \
        path.join(basedir, 'posts.db')
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
