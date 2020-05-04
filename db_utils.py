import sqlite3
from os import path

DB_FILE = 'posts.db'
with open('setup.sql', 'r') as f:
    DB_SETUP = ''.join(f.readlines())


def get_db():
    db = sqlite3.connect(DB_FILE)
    table = db.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users'")

    if table.fetchone()[0] != 1:
        db.executescript(DB_SETUP)

    return db
