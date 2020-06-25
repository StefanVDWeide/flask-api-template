from flask import request, jsonify
from app import db, jwt, limiter
from app.auth import bp
from app.models import Users, RevokedTokenModel
from app.errors.handlers import bad_request, error_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, \
    get_jwt_identity, jwt_required, get_raw_jwt
from datetime import datetime


# Checks if the JWT is on the blacklisted token list
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return RevokedTokenModel.is_jti_blacklisted(jti)


# Endpoint for adding a new user to the database
@bp.route("/register", methods=["POST"])
def register():

    if not request.is_json:
        return bad_request("Missing JSON in request")

    # Getting the data from the JSON payload
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    birthday = datetime.strptime(data["birthday"], "%Y-%m-%d")

    if not username or not password or not first_name or not last_name or not email or not birthday:
        return bad_request("Missing form parameter")

    if Users.query.filter_by(username=username).first():
        return bad_request("Username already in use")

    if Users.query.filter_by(email=email).first():
        return bad_request("Email already in use")

    user = Users(username=username,
                 first_name=first_name,
                 last_name=last_name,
                 email=email,
                 birthday=birthday)

    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Successfully registered"}), 201


# Endpoint for requesting a new access token via normal user login
@bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return bad_request("Missing JSON in request")

    # Getting all the data from the JSON payload
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    if not username or not password:
        return bad_request("Missing form parameter")

    user = Users.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return error_response(401, message="Invalid username or password")

    tokens = {"access_token": create_access_token(identity=user.id),
              "refresh_token": create_refresh_token(identity=user.id)
              }

    return jsonify(tokens), 200


# Endpoint for requesting a new access token using a valid refresh token
@bp.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    user_id = get_jwt_identity()
    new_token = create_access_token(identity=user_id, fresh=False)
    payload = {"access_token": new_token}
    return jsonify(payload), 200


# Endpoint for requesting a new fresh token
@bp.route("/fresh-login", methods=["POST"])
def fresh_login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    if not username or password:
        return bad_request("Missing form parameter")

    user = Users.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return error_response(401, message="Invalid username or password")

    new_token = create_access_token(identity=user.id, fresh=True)
    payload = {"access_token": new_token}
    return jsonify(payload), 200


# Endpoint for revoking the current user"s access token
@bp.route("/logout/token", methods=["DELETE"])
@jwt_required
def logout_access_token():
    jti = get_raw_jwt()["jti"]
    revoked_token = RevokedTokenModel(jti=jti)
    revoked_token.add()
    return jsonify({"msg": "Successfully logged out"}), 200


# Endpoint for revoking the current user"s refresh token
@bp.route("/logout/fresh", methods=["DELETE"])
@jwt_refresh_token_required
def logout_refresh_token():
    jti = get_raw_jwt()["jti"]
    revoked_token = RevokedTokenModel(jti=jti)
    revoked_token.add()
    return jsonify({"msg": "Successfully logged out"}), 200
