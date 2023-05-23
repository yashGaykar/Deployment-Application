"""APP"""
import logging
from flask import Flask
from .utility.celery_util import init_celery
from . import celery1
from .deploy_module import deploy_bp
from .onboard_module import on_board_bp
from .settings import SQLALCHEMY_DATABASE_URI

from .db import db, migrate


def create_app():
    """CREATE APPLICATION"""
    logging.basicConfig(filename='logs/app.log', filemode='a', level=logging.DEBUG,
                        format="%(asctime)s [%(threadName)-12.12s] %(levelname)s %(name)s: %(message)s")

    app = Flask(__name__)

    if app.debug:
        # Fix werkzeug handler in debug mode
        logging.getLogger('werkzeug').disabled = True

    init_celery(app, celery=celery1)

    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(deploy_bp)
    app.register_blueprint(on_board_bp)

    return app
