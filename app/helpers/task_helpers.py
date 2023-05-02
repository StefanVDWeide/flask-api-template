from rq import get_current_job

from app import db
from app.models import Tasks


def _set_task_progress(progress: int) -> None:
    """
    A helper function which updates the progress status of a background task

    Parameters
    ----------
    progress : int
        The percentage of the task progress
    """
    job = get_current_job()
    if job:
        job.meta["progress"] = progress
        job.save_meta()

        if progress >= 100:
            task = Tasks.query.filter(task_id=job.get_id()).first()
            task.complete = True

        db.session.commit()
