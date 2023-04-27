"""UTILS"""

import boto3
from flask import jsonify
from src.settings import AWS_KEY,AWS_REGION,AWS_SECRET_ACCESS_KEY

def create_client(resource:str):
    """CREATING CLIENT"""
    client = boto3.client(resource, aws_access_key_id=AWS_KEY,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
    return client


def json_response(response):
    """Json Response"""
    return jsonify({"message":response})

def error_response(message,statuscode,data=None):
    """Error Response"""
    return jsonify({"message":message,"data":data}),statuscode
