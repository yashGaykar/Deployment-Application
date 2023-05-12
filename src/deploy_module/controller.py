""" CONTROLLER FILE"""
import logging
from http import HTTPStatus
import sys
from flask import request

from src.deploy_module.exceptions import InputValidationException, ProjectAlreadyExistException, ProjectDoesNotExistException

from .schema import CleanUpSchema, DeploySchema, TaskStatusSchema
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
            raise InputValidationException(data=errors)

        logger.info(
            f"{params['project_name']}:- Checking if project with name already exists")
        infrastructure_exists = DeployService.check_project_exists(
            params["project_name"])

        if infrastructure_exists:
            raise ProjectAlreadyExistException(data=params["project_name"])
        else:
            task = deploy.apply_async(args=[params])
            logger.info(
                f"{params['project_name']}:- Started a Async Task to Deploy app with id: str(task)")
            return json_response({"id": str(task)}), HTTPStatus.OK

    except InputValidationException as error:
        logger.error(error.message, error.data)
        return error_response(error.message, error.status_code, error.data)
    except ProjectAlreadyExistException as error:
        logger.error(error.message, error.data)
        return error_response(error.message, error.status_code, error.data)


def clean_up():
    """CLEAN UP"""
    try:
        params = request.get_json()

        # Validating Inputs
        logger.info("Validating the Params")
        clean_up_schema = CleanUpSchema()
        errors = clean_up_schema.validate(params)
        if errors:
            raise InputValidationException(data=errors)

        logger.info(
            f"{params['project_name']}:- Checking if project with name doesn't exists")
        infrastructure_exists = DeployService.check_project_exists(
            params["project_name"])
        if infrastructure_exists:

            task = clean_up_task.apply_async(args=[params])
            logger.info(
                f"{params['project_name']}:- Started a Async Task to Clean Infrastructure of {params['project_name']} project with id: {task}")
            return json_response({"id": str(task)}), HTTPStatus.OK
        else:
            raise ProjectDoesNotExistException(data=params['project_name'])

    except ProjectDoesNotExistException as error:
        logger.error(error.message, error.data)
        return error_response(error.message, error.status_code, error.data)
    except InputValidationException as error:
        logger.error(error.message, error.data)
        return error_response(error.message, error.status_code, error.data)


def deploy_task_status():
    """TASK STATUS"""
    try:
        params = request.get_json()

        # Validating Inputs
        logger.info("Validating the Params")
        clean_up_schema = TaskStatusSchema()
        errors = clean_up_schema.validate(params)
        if errors:
            raise InputValidationException(data=errors)

        logger.info("Getting the status of the deploy task")
        task = deploy.AsyncResult(params["task_id"])

        response = {
            "state": task.state
        }
        if task.state != "PENDING":
            response["status"] = task.info
        logger.info(response)
        return json_response(response), HTTPStatus.OK

    except InputValidationException as error:
        logger.error(error.message, error.data)
        return error_response(error.message, error.status_code, error.data)


def clean_up_task_status():
    """CLEANUP STATUS"""
    try:
        params = request.get_json()

        # Validating Inputs
        logger.info("Validating the Params")
        clean_up_schema = TaskStatusSchema()
        errors = clean_up_schema.validate(params)
        if errors:
            raise InputValidationException(data=errors)

        logger.info("Getting the status of the deploy task")
        task = clean_up_task.AsyncResult(params["task_id"])
        response = {
            "state": task.state
        }
        if task.state != "PENDING":
            response["status"] = task.info
        logger.info(response)
        return json_response(response), HTTPStatus.OK

    except InputValidationException as error:
        logger.error(error.message, error.data)
        return error_response(error.message, error.status_code, error.data)
