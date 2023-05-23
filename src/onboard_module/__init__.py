"""INIT FILE"""

from flask import Blueprint
from src.onboard_module.controller import add_account, upload_key_pair

# Creating a Blueprint
on_board_bp = Blueprint(
    'on_board', __name__, url_prefix='/api/on_board')

# OnBoard New AWS Account
on_board_bp.add_url_rule(
    '/add_account', 'add_account', add_account, methods=['POST'])

# Upload New Key Account
on_board_bp.add_url_rule(
    '/upload_key_pair', 'upload_key_pair', upload_key_pair, methods=['POST'])
