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

        infrastructure_exists=DeployService.check_project_exists(params["project_name"])
        if infrastructure_exists:
            raise Exception("Project already Exists")
        else:
            task = deploy.apply_async(args=[params])
            return jsonify({"id": str(task)}), HTTPStatus.OK          

    except Exception as error:
        return jsonify({'error': str(error)}), HTTPStatus.BAD_REQUEST


def clean_up():
    """CLEAN UP"""
    try:
        params = request.get_json()

        infrastructure_exists=DeployService.check_project_exists(params["project_name"])
        if infrastructure_exists:
            task = clean_up_task.apply_async(args=[params])
            return jsonify({"id": str(task)}), HTTPStatus.OK
        else:
            raise Exception("Project does not Exists")

    except Exception as error:
        return jsonify({"error": str(error)}), HTTPStatus.BAD_REQUEST


def deploy_task_status():
    """TASK STATUS"""
    try:
        params = request.get_json()

        task = deploy.AsyncResult(params["id1"])

        if not task:
            raise Exception("No task Found")

        response={
            "state":task.state
        }
        if task.state!="PENDING":
            response["status"]=task.info
        return jsonify(response), HTTPStatus.OK

    except Exception as error:
        return jsonify({"error": str(error)}), HTTPStatus.BAD_REQUEST


def clean_up_task_status():
    """CLEANUP STATUS"""
    try:
        params = request.get_json()

        task = clean_up_task.AsyncResult(params["id1"])
        response={
            "state":task.state
        }
        if task.state!="PENDING":
            response["status"]=task.info
        return jsonify(response), HTTPStatus.OK

    except Exception as error:
        return jsonify({"error": str(error)}), HTTPStatus.BAD_REQUEST
