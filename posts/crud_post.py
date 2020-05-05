from itertools import count

from flask import Blueprint, request, make_response

from db_utils import get_db

crud = Blueprint('crud', __name__)


@crud.route('/')
def read_posts():
    if request.headers['Authorization'] != 'secret':
        return make_response({"error": "Bad token"}, 401)

    db = get_db()
    posts = db.execute('SELECT author, title, content FROM posts').fetchall()

    for post, i in zip(posts, count()):
        post = list(post)
        author = db.execute(f'SELECT name FROM users WHERE id={post[0]}')
        post[0] = author.fetchone()[0]

        posts[i] = {
            "author": post[0],
            "title": post[1],
            "content": post[2]
        }

    return {"posts": posts}
