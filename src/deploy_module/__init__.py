"""INIT FILE"""
from flask import Blueprint
from .controller import *

# Creating a Blueprint
deploy_bp = Blueprint(
    'deploy', __name__, url_prefix='/api/deploy')

# Deploy Node
deploy_bp.add_url_rule(
    '/deploy', 'async_deploy', async_deploy, methods=['POST'])

deploy_bp.add_url_rule(
    '/deploy_task_status', 'deploy_task_status', deploy_task_status, methods=['GET'])

deploy_bp.add_url_rule(
    '/cleanup', 'cleanup', clean_up, methods=['POST'])

deploy_bp.add_url_rule(
    '/clean_up_task_status', 'clean_up_task_status', clean_up_task_status, methods=['GET'])
