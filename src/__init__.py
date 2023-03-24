from flask import Flask, jsonify

from .deploy_module import deploy_bp

app = Flask(__name__)



app.register_blueprint(deploy_bp)


@app.route('/')
def hello1():
    """DEMO ROUTE"""
    return jsonify("Hello")