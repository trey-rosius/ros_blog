import os

from flask import Flask
from dotenv import load_dotenv
from flask_uploads import configure_uploads, patch_request_class

from flaskr.db import db
from flaskr.libs.image_helper import IMAGE_SET
from flaskr.ma import ma


def create_app(test_config=None):
    # create and configure the app
    load_dotenv(".env", verbose=True)
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='this once',
        SQLALCHEMY_DATABASE_URI="sqlite:///data.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        PROPAGATE_EXCEPTIONS=True,
        UPLOADED_IMAGES_DEST=os.path.join("flaskr/static", "images"),

        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    patch_request_class(app, 10 * 1024 * 1024)
    configure_uploads(app, IMAGE_SET)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.before_first_request
    def create_tables():
        db.create_all()

    db.init_app(app)
    ma.init_app(app)

    from .blueprints import auth, blog, contact
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    app.register_blueprint(contact.bp)

    return app
