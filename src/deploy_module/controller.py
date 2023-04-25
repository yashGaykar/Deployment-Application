""" CONTROLLER FILE"""
from http import HTTPStatus
from flask import jsonify, request

from .schema import DeploySchema
from .tasks import deploy, clean_up_task
from .service import DeployService


def async_deploy():
    """ASYNC DEPLOY"""
    try:
        params = request.get_json()

        # Validating Inputs
        deploy_schema = DeploySchema()
        errors = deploy_schema.validate(params)
        if errors:
            raise Exception(errors)

        task = deploy.apply_async(args=[params])
        return jsonify({"id": str(task)}), HTTPStatus.OK

    except Exception as error:
        return jsonify({'error': str(error)}), HTTPStatus.BAD_REQUEST


def clean_up():
    """CLEAN UP"""
    try:
        params = request.get_json()

        # Validating Inputs
        deploy_schema = DeploySchema()
        errors = deploy_schema.validate(params)
        if errors:
            raise Exception(errors)

        # task = clean_up_task.apply_async(args=[params])
        # return jsonify({"id": str(task)}), HTTPStatus.OK

        # Variables to be passed for terraform
        terraform_env = DeployService.terraform_env(params["port"])

        # return("hello")
        out = DeployService.execute_command(
            ['terraform', 'destroy', '-force'], f'./infras/{params["project_name"]}', terraform_env)
        return out

    except Exception as error:
        return jsonify({"error": str(error)}), HTTPStatus.BAD_REQUEST


def taskstatus():
    """TASK STATUS"""
    try:
        params = request.get_json()

        task = deploy.AsyncResult(params["id1"])
        if not task:
            raise Exception("No task Found")

        if task.state == 'PENDING':
            response = {
                'state': task.state,
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'status': str(task.info),
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            response = {
                'state': task.state,
                'status': str(task.info),
            }
        return jsonify(response), HTTPStatus.OK

    except Exception as error:
        return jsonify({"error": str(error)}), HTTPStatus.BAD_REQUEST


def cleanup_taskstatus():
    """CLEANUP STATUS"""
    try:
        params = request.get_json()

        task = clean_up_task.AsyncResult(params["id1"])
        return jsonify({"x": task}), HTTPStatus.OK

    except Exception as error:
        return jsonify({"error": str(error)}), HTTPStatus.BAD_REQUEST
