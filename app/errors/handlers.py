from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


# A catch all function which returns the error code and message back to the user
def error_response(status_code, message=None):
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    if message:
        payload["msg"] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


# Returns a 400 error code when a bad request has been made
def bad_request(message):
    return error_response(400, message)
