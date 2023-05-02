import sys
from datetime import time

from app import create_app
from app.helpers.task_helpers import _set_task_progress

# Create the app in order to operate within the context of the app
app = create_app()


def count_seconds(**kwargs: int) -> None:
    """
    A background task which counts up to the number of seconds passed as an argument
    """
    with app.app_context():
        try:
            number: int | None = kwargs.get("number")

            if number:
                _set_task_progress(0)

                i = 0

                for i in range(0, number):
                    i += 1
                    time.sleep(1)
                    _set_task_progress(100 * i // number)

        # TODO: Make this a specific except type, no bare except
        except:
            app.logger.error("Unhandled exception", exc_info=sys.exc_info())

        finally:
            _set_task_progress(100)
