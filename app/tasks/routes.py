from flask import Response, jsonify
from flask_jwt_extended import current_user, jwt_required

from app import db
from app.errors.handlers import bad_request
from app.schemas import TasksSchema
from app.tasks import bp

tasks_schema = TasksSchema(many=True)


@bp.get("/background-task/count-seconds/<int:number>")
@jwt_required()
def background_worker_count_seconds(number: int) -> tuple[Response, int] | Response:
    """
    Spawn a background task via RQ to perform a long running task

    Parameters
    ----------
    number : int
        The number of seconds the background tasks needs to count

    Returns
    -------
    JSON
        A JSON object containing either the success message or an error message
    """
    if current_user.get_task_in_progress("count_seconds"):
        return bad_request("Task already in progress")

    else:
        current_user.launch_task("count_seconds", "Counting seconds...", number=number)
        db.session.commit()

    return jsonify({"msg": "Launched background task"}), 200


@bp.get("/get/active-background-tasks")
@jwt_required()
def active_background_tasks() -> tuple[Response, int] | str:
    """
    Endpoint to retrieve all the active background tasks

    Returns
    -------
    str
        A JSON object containing the active tasks
    """
    tasks = current_user.get_tasks_in_progress()
    return tasks_schema.jsonify(tasks), 200


@bp.get("/get/finished-background-tasks")
@jwt_required()
def finished_background_tasks() -> tuple[Response, int] | str:
    """
    Endpoint to retrieve the finished background tasks

    Returns
    -------
    str
        A JSON object containing the finished tasks
    """
    tasks = current_user.get_completed_tasks()
    return tasks_schema.jsonify(tasks), 200
