from flask.helpers import get_debug_flag
from . import celery1
from .app import create_app
from .utility.celery_util import init_celery

app = create_app()
init_celery(app, celery1)