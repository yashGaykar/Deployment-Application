
import tempfile


from ..utils  import create_client
from .service import DeployService,RunPlaybookService
from settings import *


from .. import celery1

@celery1.task
def deploy(params):
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
        
        # Remove the temporary inventory file
        os.remove(inventory_file.name)


        if params["app_type"]=="flask":
            # deploy a flask app
            output =deploy_service.run_playbook('./templates/flask_deploy.yml')
            print(output)


        elif params["app_type"]=="node":

            # deploy a node app
            output =deploy_service.run_playbook('./templates/node_deploy.yml')
            print(output)

        else:
            raise Exception("Invalid App Type")
        
        if(output==0):
            return (f"Successfully Deployed the Application at http://{public_ip}:3000")
        else:
            raise Exception("Failed to Deploy the Application")


