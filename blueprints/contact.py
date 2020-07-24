from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_uploads import UploadNotAllowed

from flaskr.blueprints.auth import login_required, get_post
from flaskr.libs import image_helper
from flaskr.models.post import PostModel
from flaskr.models.user import UserModel

bp = Blueprint('contact', __name__)
@bp.route('/contact')
def send_email():

    return render_template('contact/contact.html')
