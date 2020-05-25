from datetime import datetime, timedelta
from flask import Blueprint, request, make_response, redirect

from util import have
from ..auth import auth
from ..models import db, Post
from ..limiter import limiter


crud = Blueprint('crud', __name__)


@crud.route('/create', methods=['POST'])
@auth.login_required
@limiter.limit('20/hour')
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


@crud.route('/')
@auth.login_required
def read_posts():
    posts = [post.to_dict() for post in Post.query.all()]

    return {"posts": posts}


@crud.route('/<int:n>')
@auth.login_required
def read_post(n):
    return Post.query.filter_by(id=n).first().to_dict()


@crud.route('/<int:n_min>-<int:n_max>')
@auth.login_required
def read_n_posts(n_min, n_max):
    if n_min > n_max:
        return make_response({"error":
                              "Min must be less or equal tham max"}, 400)
    elif n_min == n_max:
        return redirect(f'/posts/{n_max}')

    posts = Post.query.filter(Post.id >= n_min).filter(Post.id <= n_max).all()
    posts = [post.to_dict() for post in posts]

    return {"posts": posts}


@crud.route('/delete/<int:post_id>', methods=['DELETE'])
@auth.login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).one()

    if post.author == auth.current_user():
        db.session.delete(post)
        db.session.commit()
        return {'data': True}

    return make_response({"error": "Access denied"}, 401)
