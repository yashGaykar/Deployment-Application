"""CELERY UTILS"""


def init_celery(app, celery):
    """Add flask app context to celery.Task"""
    task_base = celery.Task

    class ContextTask(task_base):
        """CREATE UTILS"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
