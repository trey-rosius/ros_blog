from flaskr.ma import ma
from flaskr.models.post import PostModel


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PostModel
        include_fk=True
        load_instance=True
