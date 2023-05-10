""" CONTROLLER FILE"""
import logging
from http import HTTPStatus
import sys
from flask import request

from src.deploy_module.exceptions import CommandExecutionFailed, DeployValidationException, DeploymentFailedException, ProjectAlreadyExistException, ProjectDoesNotExistException

from .schema import DeploySchema
from .tasks import deploy, clean_up_task
from .service import DeployService
from ..utils import json_response, error_response

# Creating Logger object
logger = logging.getLogger("deploy")
logger.addHandler(logging.StreamHandler(sys.stdout))


def async_deploy():
    """ASYNC DEPLOY"""
    try:
        params = request.get_json()

        # Validating Inputs
        logger.info("Validating the Params")
        deploy_schema = DeploySchema()
        errors = deploy_schema.validate(params)
        if errors:
            raise DeployValidationException(data=errors)

        logger.info("Checking if project with name already exists")
        infrastructure_exists = DeployService.check_project_exists(
            params["project_name"])

        if infrastructure_exists:
            raise ProjectAlreadyExistException(data=params["project_name"])
        else:
            task = deploy.apply_async(args=[params])
            logger.info(
                "Started a Async Task to Deploy app with id: %s", str(task))
            return json_response({"id": str(task)}), HTTPStatus.OK

    except DeployValidationException as error:
        logger.error(error.message, error.data)
        return error_response(error.message, error.status_code, error.data)
    except ProjectAlreadyExistException as error:
        logger.error(error.message, error.data)
        return error_response(error.message, error.status_code, error.data)
    except DeploymentFailedException as error:
        logger.error((error.message))
        return error_response(error.message, error.status_code)
    except CommandExecutionFailed as error:
        logger.error(error.message, error.data)
        return error_response(error.message, error.status_code)
    except Exception as error:
        logger.error(str(error))
        return error_response(str(error), HTTPStatus.BAD_REQUEST)


def clean_up():
    """CLEAN UP"""
    try:
        params = request.get_json()

        logger.info("Checking if project with name doesn't exists")
        infrastructure_exists = DeployService.check_project_exists(
            params["project_name"])
        if infrastructure_exists:

            task = clean_up_task.apply_async(args=[params])
            logger.info(
                "Started a Async Task to Clean Infrastructure of %s project with id: %s", params['project_name'], task)
            return json_response({"id": str(task)}), HTTPStatus.OK
        else:
            raise ProjectDoesNotExistException(data=params['project_name'])

    except ProjectDoesNotExistException as error:
        logger.error(error.message, error.data)
        return error_response(error.message, error.status_code, error.data)
    except CommandExecutionFailed as error:
        logger.error(error.message, error.data)
        return error_response(error.message, error.status_code)
    except Exception as error:
        logger.error(str(error))
        return error_response(str(error), HTTPStatus.BAD_REQUEST)


def deploy_task_status():
    """TASK STATUS"""
    try:
        params = request.get_json()

        logger.info("Getting the status of the deploy task")
        task = deploy.AsyncResult(params["id1"])

        response = {
            "state": task.state
        }
        if task.state != "PENDING":
            response["status"] = task.info
        logger.info(response)
        return json_response(response), HTTPStatus.OK

    except Exception as error:
        logger.error(str(error))
        return error_response(str(error), HTTPStatus.BAD_REQUEST)


def clean_up_task_status():
    """CLEANUP STATUS"""
    try:
        params = request.get_json()

        logger.info("Getting the status of the deploy task")
        task = clean_up_task.AsyncResult(params["id1"])
        response = {
            "state": task.state
        }
        if task.state != "PENDING":
            response["status"] = task.info
        logger.info(response)
        return json_response(response), HTTPStatus.OK

    except Exception as error:
        logger.error(str(error))
        return error_response(str(error), HTTPStatus.BAD_REQUEST)
