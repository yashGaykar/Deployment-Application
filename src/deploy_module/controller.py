from flask import jsonify,request
import time
import tempfile

from ..utils  import create_client
from .service import DeployService,RunPlaybookService
from .schema import DeploySchema
from settings import *

def deploy():
    

    try:
        params=request.get_json()

        # Validating Inputs
        deploy_schema = DeploySchema()
        errors = deploy_schema.validate(params)
        if errors:
            raise Exception(errors)

        # creates EC2 client
        ec2 =create_client("ec2")

        if ('instance_id' not in params.keys()):
            instance_id=DeployService.create_instance(ec2)
        else:
            instance_id=params['instance_id']

        instance_info = ec2.describe_instances(InstanceIds=[instance_id])

        public_ip=instance_info["Reservations"][0]["Instances"][0]["NetworkInterfaces"][0]["Association"]["PublicIp"]

        env=params['env'] if ('env' in params.keys()) else {}
        # temporary inventary file content
        variables={'app_repo_url':params["git"], 'env' : env}

        file=f"[ec2_instances]\n{public_ip}\n\n[ec2_instances:vars]\n"
        for key,value in variables.items():
            file+=f'{key}={value}\n'

        # temporary inventary file
        inventory_file = tempfile.NamedTemporaryFile(delete=False)
        inventory_file.write(file.encode('utf-8'))
        inventory_file.close()

        deploy_service=RunPlaybookService(inventory_file)


        if params["app_type"]=="flask":
            # deploy a flask app
            output =deploy_service.run_playbook('./src/deploy_module/templates/flask_deploy.yml')
            return jsonify(output)

        elif params["app_type"]=="node":
            # deploy a node app

            output =deploy_service.run_playbook('./src/deploy_module/templates/node_deploy.yml')
            return jsonify(output)

        # else:
        #     raise Exception("Invalid App Type")

    except Exception as e:
        return jsonify({"error":str(e)})



# Parameters={'commands': ["sudo apt-get update","sudo apt-get install nodejs -y","sudo apt-get install npm -y","cd ../../../../home/ubuntu/","git clone https://github.com/yashGaykar/nodejs_practice.git","cd nodejs_practice","npm i","sudo su","echo 'export DATABASE_URI=mongodb+srv://yashgaykar:Gaya%40193@cluster0.nj9yven.mongodb.net/?retryWrites=true&w=majority' >> ~/.bashrc","echo 'export JWT_SECRET_KEY=SecretKey' >> ~/.bashrc"]},
