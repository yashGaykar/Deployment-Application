"""APP"""
import logging
from flask import Flask
from .utility.celery_util import init_celery
from . import celery1
from .deploy_module import deploy_bp


def create_app():
    """CREATE APPLICATION"""
    logging.basicConfig(filename='logs/app.log', filemode='a', level=logging.DEBUG,
                format="%(asctime)s [%(threadName)-12.12s] %(levelname)s %(name)s: %(message)s")
    app = Flask(__name__)
    if app.debug:
        # Fix werkzeug handler in debug mode
        logging.getLogger('werkzeug').disabled = True
    init_celery(app, celery=celery1)
    app.register_blueprint(deploy_bp)
    return app
