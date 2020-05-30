from app.main import bp
from app.models import Users, UsersSchema
from app.errors.handlers import bad_request
from flask_jwt_extended import jwt_required, current_user


# Declare database schemas so they can be returned as JSON objects
user_schema = UsersSchema(exclude=("email", "password_hash"))
users_schema = UsersSchema(many=True, exclude=("email", "password_hash"))


# Render main user calendar page
@bp.route('/', methods=['GET'])
@jwt_required
def api_main_calendar():
    user = current_user
    return user_schema.jsonify(user)


# Lets users go to a profile page
@bp.route('/user/<username>', methods=['GET'])
@jwt_required
def api_user(username):
    user = Users.query.filter_by(username=username).first()

    if user is None:
        return bad_request("User not found")

    return user_schema.jsonify(user)
