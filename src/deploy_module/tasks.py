"""TASKS"""

import tempfile
import time
import os

from .service import RunPlaybookService
from .service import DeployService

from .. import celery1
from .constants import PROJECT_EXISTS, TERRAFORM_FILE, ANSIBLE_FLASK_TEMPLATE
from .constants import ANSIBLE_NODE_TEMPLATE, INVALID_APP, DEPLOYMENT_FAILED


# @celery1.task(task_time_limit=600,max_retries=0,timeout=600)
@celery1.task()
def deploy(params):
    """DEPLOY"""

    DeployService.execute_command(
        ['mkdir', f'{params["project_name"]}'], './infras')
    DeployService.execute_command(
        ['cp', TERRAFORM_FILE, f'./infras/{params["project_name"]}'], './')
    DeployService.execute_command(
        ['terraform', 'init'], f'./infras/{params["project_name"]}')

    # Variables to be passed for terraform
    terraform_env = DeployService.terraform_env(params["port"])

    # create infra-structure
    output = DeployService.execute_command(
        ['terraform', 'apply', '--auto-approve'],
        f'./infras/{params["project_name"]}',
        terraform_env)
    public_ip = output[0][-18:].split("\"")[1]

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
    inventory_file = tempfile.NamedTemporaryFile(delete=False)
    inventory_file.write(file.encode('utf-8'))
    inventory_file.close()

    deploy_service = RunPlaybookService(inventory_file)

    # Remove the temporary inventory file
    os.remove(inventory_file.name)

    if params["app_type"] == "flask":
        # deploy a flask app
        output = deploy_service.run_playbook(ANSIBLE_FLASK_TEMPLATE)
        print(output)

    elif params["app_type"] == "node":
        # deploy a node app
        output = deploy_service.run_playbook(ANSIBLE_NODE_TEMPLATE)
        print(output)

    else:
        raise Exception(INVALID_APP)

    if output == 0:
        return f"Successfully Deployed the Application on instance at http://{public_ip}:{port} "
    else:
        raise Exception(DEPLOYMENT_FAILED)


@celery1.task()
def clean_up_task(params):
    """Variables to be passed for terraform"""
    terraform_env = DeployService.terraform_env("3000")

    DeployService.execute_command(
        ['terraform', 'destroy', '--auto-approve'],
        f'./infras/{params["project_name"]}',
        terraform_env)
    DeployService.delete_project_folder(params["project_name"])
    return f"Successfully Cleaned up the Infrastructure for project {params['project_name']}"
