from flask import Blueprint, request, make_response, redirect

from db_utils import get_db
from auth import auth

crud = Blueprint('crud', __name__)
@crud.route('/count')
def get_count():
    db = get_db()
    posts = db.execute('SELECT count(*) from posts').fetchone()

    return str(posts[0])


@crud.route('/')
@auth.login_required
def read_posts():
    db = get_db()
    posts = db.execute('SELECT author, title, content FROM posts').fetchall()

    posts = [add_author_info(db, post) for post in posts]

    return {"posts": posts}


@crud.route('/<int:n>')
@auth.login_required
def read_post(n):
    if n > int(get_count()):
        return make_response({"error": "Post doesn't exists"}, 404)

    db = get_db()
    post = db.execute(f'SELECT author, title, content FROM posts WHERE id={n}')

    return add_author_info(db, post.fetchone())


@crud.route('/<int:n_min>-<int:n_max>')
@auth.login_required
def read_n_posts(n_min, n_max):
    if n_min > n_max:
        return make_response({"error": "Min must be less or equal tham max"}, 400)
    elif n_min == n_max:
        return redirect(f'/posts/{n_max}')

    db = get_db()
    posts = db.execute(
        f'SELECT author, title, content FROM posts WHERE id>={n_min} AND id<={n_max}')

    posts = [add_author_info(db, post) for post in posts.fetchall()]

    return {"posts": posts}


def add_author_info(db, post):
    post = list(post)
    author = db.execute(f'SELECT name FROM users WHERE id={post[0]}')
    post[0] = author.fetchone()[0]

    return {"author": post[0], "title": post[1], "content": post[2]}
