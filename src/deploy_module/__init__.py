from flask import Blueprint
from .controller import *



# Creating a Blueprint
deploy_bp = Blueprint(
    'deploy', __name__, url_prefix='/api/deploy')


# Deploy Node
deploy_bp.add_url_rule(
    '/deploy', 'deploy', deploy, methods=['POST'])

