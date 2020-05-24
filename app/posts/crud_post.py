import uuid0
from datetime import datetime, timedelta
from flask import Blueprint, request, make_response, redirect

from ..auth import auth
from ..models import db, Post, User
from util import have


crud = Blueprint('crud', __name__)


@crud.route('/create', methods=['POST'])
@auth.login_required
def create_post():
    data = request.json

    if not have(data, ['title', 'content']):
        return make_response({"error": 'Title or content wasn\'t provided'}, 400)

    date_format = '%y-%m-%d %H:%M'
    now = datetime.now().strftime(date_format)
    ten_minutes = timedelta(minutes=10)
    latest_post = auth.current_user().posts[-1]

    if latest_post is not None and datetime.now() - datetime.strptime(latest_post.created_at, date_format) < ten_minutes:
        return {"error": "You can public only one post for each ten minutes"}

    new_post = Post(
        uuid=str(uuid0.generate()),
        title=data["title"],
        content=data["content"],
        created_at=now
    )
    auth.current_user().posts.append(new_post)
    db.session.commit()

    return {'data': True}


@crud.route('/count')
def get_count():
    return str(Post.query.count())


# @crud.route('/')
# @auth.login_required
# def read_posts():
#     db = get_db()
#     posts = db.execute('SELECT author, title, content FROM posts').fetchall()

#     posts = [add_author_info(db, post) for post in posts]

#     return {"posts": posts}
