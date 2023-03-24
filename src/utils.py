import boto3
from settings import *

def create_client(resource:str):
    client = boto3.client(resource, aws_access_key_id=AWS_KEY,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
    return client