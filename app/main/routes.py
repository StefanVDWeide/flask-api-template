from app.main import bp
from app.models import Users, UsersSchema
from app.errors.handlers import bad_request
from flask_jwt_extended import jwt_required, current_user


# Declare database schemas so they can be returned as JSON objects
user_schema = UsersSchema(exclude=("email", "password_hash"))
users_schema = UsersSchema(many=True, exclude=("email", "password_hash"))


# Let's users retrieve their own user information when logged in
@bp.route("/", methods=["GET"])
@jwt_required()
def user_page():
    user = current_user
    return user_schema.jsonify(user)


# Lets users retrieve a user profile when logged in
@bp.route("/user/<username>", methods=["GET"])
@jwt_required()
def get_user(username):
    user = Users.query.filter_by(username=username).first()

    if user is None:
        return bad_request("User not found")

    return user_schema.jsonify(user)
