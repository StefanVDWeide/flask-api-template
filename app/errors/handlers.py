from flask import Response, jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code: int, message=None) -> Response:
    """
    A catch all function which returns the error code and message back to the user

    Parameters
    ----------
    status_code : int
        The HTTP status code
    message : str, optional
        The error message, by default None

    Returns
    -------
    str
        A JSON object containing the error information and HTTP code
    """
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}

    if message:
        payload["msg"] = message

    response = jsonify(payload)
    response.status_code = status_code

    return response


def bad_request(message: str) -> Response:
    """
    Returns a 400 error code when a bad request has been made

    Parameters
    ----------
    message : str
        The error message

    Returns
    -------
    str
        A JSON object containing the error message and a 400 HTTP code
    """
    return error_response(400, message)
