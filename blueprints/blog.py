import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,jsonify
)
from flask_uploads import UploadNotAllowed


from flaskr.blueprints.auth import login_required, get_post
from flaskr.libs import image_helper
from flaskr.models.post import PostModel
from flaskr.models.user import UserModel
from flaskr.schema.post import PostSchema

bp = Blueprint('blog', __name__)

post_schema = PostSchema()
@bp.route('/post/json')
def allPosts():
    
    return {"posts": post_schema.dump(PostModel.find_all_posts(), many=True)}, 200


@bp.route('/')
def index():
    posts = PostModel.find_all_posts()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        image_file = request.files['file']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        if not image_file:
            flash("Please Attach a file")
        else:

            folder = f"user_{g.user.id}"  # static/images
            try:
                image_path = image_helper.save_image(image_file,
                                                     folder=folder)
                basename = image_helper.get_path(image_path)
                userModel = UserModel.find_user_by_id(g.user.id)
                post = PostModel(title=title, posts=body, image_url=image_path, user_id=userModel.id)
                post.save_to_db()

            except UploadNotAllowed:
                extension = image_helper.get_extension(image_file)
                flash("file with extension {} not allowed".format(extension))

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.posts = body
            post.save_to_db()

            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    post.delete()
    return redirect(url_for('blog.index'))
