from flask import jsonify, request
from http import HTTPStatus

from .schema import DeploySchema

from src.settings import *
from .tasks import deploy
from .service import DeployService


def async_deploy():
    try:
        params = request.get_json()

        # Validating Inputs
        deploy_schema = DeploySchema()
        errors = deploy_schema.validate(params)
        if errors:
            raise Exception(errors)

        task = deploy.apply_async(args=[params])
        return jsonify({"id": str(task)}), HTTPStatus.OK

    except Exception as e:
        return jsonify({'error': str(e)}),HTTPStatus.BAD_REQUEST


def clean_up():
    params = request.get_json()

    out = DeployService.execute_command(
        ['terraform', 'destroy', '--force'], f'./infras/{params["project_name"]}',)
    print(out)
    return jsonify(out)


def taskstatus():
    try:
        params = request.get_json()

        task = deploy.AsyncResult(params["id1"])
        if (not task):
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

    except Exception as e:
        return jsonify({"error":str(e)}),HTTPStatus.BAD_REQUEST

        