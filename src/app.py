from flask import Flask, jsonify
from .utility.celery_util import init_celery
from . import celery1
from .deploy_module import deploy_bp


def create_app():

    app = Flask(__name__)
    init_celery(app, celery=celery1)
    app.register_blueprint(deploy_bp)
    return app
