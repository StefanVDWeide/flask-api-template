from app.users import bp
from app.models import Users
from app.schemas import UsersSchema
from app.errors.handlers import bad_request
from flask_jwt_extended import jwt_required, current_user


# Declare database schemas so they can be returned as JSON objects
user_schema = UsersSchema(exclude=("email", "password_hash"))
users_schema = UsersSchema(many=True, exclude=("email", "password_hash"))


@bp.get("/get/user/profile")
@jwt_required()
def user_page() -> str:
    """
    Let's users retrieve their own user information when logged in

    Returns
    -------
    str
        A JSON object containing the user profile information
    """
    return user_schema.jsonify(current_user), 200


@bp.get("/get/user/profile/<string:username>")
@jwt_required()
def get_user(username: str) -> str:
    """
    Lets users retrieve a user profile when logged in

    Parameters
    ----------
    username : str
        The username of the user who's information should be retrieved

    Returns
    -------
    str
        A JSON object containing the user profile information
    """
    user = Users.query.filter_by(username=username).first()

    if user is None:
        return bad_request("User not found")

    return user_schema.jsonify(user), 200
