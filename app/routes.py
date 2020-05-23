from flask import Flask, current_app as app

# Declare 'app' type
app: Flask = app


@app.route('/')
def index():
    return "ok"
