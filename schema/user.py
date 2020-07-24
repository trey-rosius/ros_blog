from flaskr.ma import ma
from flaskr.models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = UserModel
        load_only=("password",)
        load_instance=True
