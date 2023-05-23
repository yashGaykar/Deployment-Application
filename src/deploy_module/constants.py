"""CONSTANTS FILE
"""
INSTANCE_AMI = "ami-0557a15b87f6559cf"
AWS_REGION = "us-east-1"
INSTANCE_TYPE = "t2.micro"
IMAGE_ID = "ami-0557a15b87f6559cf"
INSTANCE_USER_NAME="ubuntu"

ANSIBLE_FLASK_TEMPLATE = './templates/ansible/flask_deploy.yml'
ANSIBLE_NODE_TEMPLATE = './templates/ansible/node_deploy.yml'
TERRAFORM_FILE = './templates/terraform/main.tf'


PROJECT_EXISTS = "Project already exists with the given name"
INVALID_APP = "Invalid App Type"
DEPLOYMENT_FAILED = "Failed to Deploy the Application"
