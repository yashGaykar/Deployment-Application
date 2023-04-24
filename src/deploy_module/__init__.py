from flask import Blueprint
from .controller import *



# Creating a Blueprint
deploy_bp = Blueprint(
    'deploy', __name__, url_prefix='/api/deploy')


# Deploy Node
deploy_bp.add_url_rule(
    '/deploy', 'async_deploy', async_deploy, methods=['POST'])

deploy_bp.add_url_rule(
    '/taskstatus','taskstatus', taskstatus, methods=['GET']
)

deploy_bp.add_url_rule(
    '/cleanup','cleanup', clean_up, methods=['POST']
)


