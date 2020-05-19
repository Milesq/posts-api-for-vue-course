import uuid0

from datetime import datetime, timedelta

from flask import Blueprint, request, make_response, redirect

from db_utils import get_db
from auth import auth
from util import have


crud = Blueprint('crud', __name__)


@crud.route('/delete/<int:post_uuid>', methods=['DELETE'])
@auth.login_required
def delete_post(post_uuid):
    db = get_db()
    db.execute(f'DELETE FROM posts WHERE uuid={post_uuid}')
    return {'data': True}


@crud.route('/create', methods=['POST'])
@auth.login_required
def create_post():
    data = request.json

    if not have(data, ['title', 'content']):
        return make_response({"error":
                              'Title or content wasn\'t provided'}, 400)

    date_format = '%y-%m-%d %H:%M'
    db = get_db()
    latest_post = db.execute(f'''
        SELECT created_at
        FROM posts
        WHERE author={auth.current_user()}
        ORDER BY created_at DESC
        LIMIT 1
    ''').fetchone()[0]

    ten_minutes = timedelta(minutes=10)

    if datetime.now() - datetime.strptime(latest_post, date_format) < ten_minutes:
        return {"error": "You can public only one post for each ten minutes"}

    now = datetime.now().strftime(date_format)
    db.execute(f"""
        INSERT INTO posts(uuid, author, title, content, created_at)
        VALUES (
            {uuid0.generate()},
            {auth.current_user()},
            "{data["title"]}",
            "{data["content"]}",
            "{now}"
        )
    """)
    db.commit()

    return {'data': True}


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


@crud.route('/<str:uuid>')
@auth.login_required
def read_post(uuid):
    db = get_db()
    uuid_exists = db.execute(f'SELECT uuid FROM posts WHERE uuid={uuid}')
    if not uuid_exists:
        return make_response({"error": "Post doesn't exists"}, 404)

    post = db.execute(f'SELECT author, title, content FROM posts WHERE uuid={uuid}')

    return add_author_info(db, post.fetchone())


@crud.route('/<int:n_min>-<int:n_max>')
@auth.login_required
def read_n_posts(n_min, n_max):
    if n_min > n_max:
        return make_response({"error":
                              "Min must be less or equal tham max"}, 400)
    elif n_min == n_max:
        return redirect(f'/posts/{n_max}')

    db = get_db()
    posts = db.execute(f'''
        SELECT author, title, content
        FROM posts
        WHERE id>={n_min} AND id<={n_max}
    ''')

    posts = [add_author_info(db, post) for post in posts.fetchall()]

    return {"posts": posts}


def add_author_info(db, post):
    post = list(post)
    author = db.execute(f'SELECT name FROM users WHERE id={post[0]}')
    post[0] = author.fetchone()[0]

    return {"author": post[0], "title": post[1], "content": post[2]}
