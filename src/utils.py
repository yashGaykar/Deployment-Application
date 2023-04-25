"""UTILS"""

import boto3
from src.settings import AWS_KEY,AWS_REGION,AWS_SECRET_ACCESS_KEY

def create_client(resource:str):
    """CREATING CLIENT"""
    client = boto3.client(resource, aws_access_key_id=AWS_KEY,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
    return client
