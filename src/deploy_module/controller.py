from flask import jsonify,request
from http import HTTPStatus

from .schema import DeploySchema

from settings import *
from .tasks import deploy



def async_deploy():
    params=request.get_json()

    # Validating Inputs
    deploy_schema = DeploySchema()
    errors = deploy_schema.validate(params)
    if errors:
        raise Exception(errors)

    task=deploy.apply_async(args=[params])
    return jsonify({"id":str(task)}),HTTPStatus.OK

def taskstatus():
    params=request.get_json()

    task = deploy.AsyncResult(params["id1"])
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
    return jsonify(response)


