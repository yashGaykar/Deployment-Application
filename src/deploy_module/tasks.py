"""TASKS"""

import logging
import sys
import tempfile
import time
import os

from src.deploy_module.exceptions import DeploymentFailedException

from .service import RunPlaybookService
from .service import DeployService

from .. import celery1
from .constants import TERRAFORM_FILE, ANSIBLE_FLASK_TEMPLATE
from .constants import ANSIBLE_NODE_TEMPLATE

from celery.utils.log import get_task_logger

from ..onboard_module.models import AWSAccount

# Set up logging for Flask and Celery
formatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] %(levelname)s %(name)s: %(message)s")
file_handler = logging.FileHandler('logs/app.log')
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Set up Celery logging
logger = get_task_logger(__name__)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

# @celery1.task(task_time_limit=600,max_retries=0,timeout=600)
@celery1.task()
def deploy(params):
    """DEPLOY"""

    account = AWSAccount.query.get(params["account_id"])
    if account.key_name is None:
        raise Exception("Key has not been uploaded for the account")

    logger.info(f"{params['project_name']}:- Creating Folder for project terraform details")
    DeployService.execute_command(
        ['mkdir', f'{params["project_name"]}'], './infras')
    DeployService.execute_command(
        ['cp', TERRAFORM_FILE, f'./infras/{params["project_name"]}'], './')
    DeployService.execute_command(
        ['terraform', 'init'], f'./infras/{params["project_name"]}')

    # Variables to be passed for terraform
    terraform_env = DeployService.terraform_env(params["port"], params["project_name"], account)

    logger.info(f"{params['project_name']}:- Creating the Infrastructure to deploy the Application")
    # create infra-structure
    output = DeployService.execute_command(
        ['terraform', 'apply', '--auto-approve'],
        f'./infras/{params["project_name"]}',
        terraform_env)
    public_ip = output[0][-18:].split("\"")[1]
    logger.info(f"{params['project_name']}:- Created the Infrastructure with Public IP: {public_ip}")

    env = params['env'] if ('env' in params.keys()) else {}

    port = params['port']
    env['PORT'] = port

    # temporary inventary file content
    variables = {'app_repo_url': params["git"], 'env': env, 'port': port}

    file = f"[ec2-instances]\n{public_ip}\n\n[ec2-instances:vars]\n"
    for key, value in variables.items():
        file += f'{key}={value}\n'
    time.sleep(20)

    # temporary inventary file
    logger.info(f"{params['project_name']}:- Creating the Temporary Inventory File")
    inventory_file = tempfile.NamedTemporaryFile(delete=False)
    inventory_file.write(file.encode('utf-8'))
    inventory_file.close()

    logger.info(f"{params['project_name']}:- Passed Inventory file to playbook")
    deploy_service = RunPlaybookService(inventory_file, params["project_name"], terraform_env["TF_VAR_instance_key"])


    # Remove the temporary inventory file
    logger.info(f"{params['project_name']}:- Removing Temporary Inventory File")
    os.remove(inventory_file.name)

    if params["app_type"] == "flask":
        # deploy a flask app
        logger.info(f"{params['project_name']}:- Running a Flask Playbook")
        output = deploy_service.run_playbook(ANSIBLE_FLASK_TEMPLATE)
        print(output)

    # elif params["app_type"] == "node":
    else:
        # deploy a node app
        logger.info(f"{params['project_name']}:- Running a Node Playbook")
        output = deploy_service.run_playbook(ANSIBLE_NODE_TEMPLATE)
        print(output)

    if output == 0:
        success_message = f"{params['project_name']}:- Successfully Deployed the Application on instance at http://{public_ip}:{port} "
        logger.info(success_message)
        return success_message
    else:
        raise Exception(f"{params['project_name']}:- Deployment Failed for the Application")


@celery1.task()
def clean_up_task(params):
    """Variables to be passed for terraform"""

    account = AWSAccount.query.get(params["account_id"])

    terraform_env = DeployService.terraform_env("3000",params["project_name"], account)

    logger.info(f"{params['project_name']}:- Destroying the Infrastructure")
    DeployService.execute_command(
        ['terraform', 'destroy', '--auto-approve'],
        f'./infras/{params["project_name"]}',
        terraform_env)
    logger.info(f"{params['project_name']}:- Deleting the Project Folder in the App")
    DeployService.delete_project_folder(params["project_name"])
    success_message = f"{params['project_name']}:- Successfully Cleaned up the Infrastructure for project {params['project_name']}"
    logger.info(success_message)
    return success_message
