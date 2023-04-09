
import tempfile
import time
import subprocess
import os
import configparser


from ..utils  import create_client
from .service import DeployService,RunPlaybookService
from src.settings import *




from .. import celery1
from ..settings import AWS_REGION,AWS_SECRET_ACCESS_KEY,AWS_KEY,INSTANCE_KEY,INSTANCE_TYPE


@celery1.task(time_limit=400)
def  deploy(params):

            path=os.getcwd()
            out=DeployService.execute_command(['mkdir',f'{params["project_name"]}'],f'{path}/infras')
            if (out) and ("File exist" in out[0]) :
                raise Exception("Project Already Exists")        
            DeployService.execute_command(['cp','./templates/terraform/main.tf',f'./infras/{params["project_name"]}'],f'{path}')
            DeployService.execute_command(['terraform','init'],f'{path}/infras/{params["project_name"]}')
            terraform_env={
                "TF_VAR_aws_region":AWS_REGION,
                "TF_VAR_aws_access_key":AWS_KEY,
                "TF_VAR_aws_secret_access_key":AWS_SECRET_ACCESS_KEY,
                "TF_VAR_app_port":params['port'],
                "TF_VAR_instance_ami":"ami-0557a15b87f6559cf",
                "TF_VAR_instance_key":INSTANCE_KEY,
                "TF_VAR_instance_type":INSTANCE_TYPE,
            }

            output=DeployService.execute_command(['terraform','apply','--auto-approve'],f'{path}/infras/{params["project_name"]}',terraform_env)
            public_ip=output[0][-18:].split("\"")[1]
            time.sleep(30)


            env=params['env'] if ('env' in params.keys()) else {}

            port= params['port']
            env['PORT']=port

            # temporary inventary file content
            variables={'app_repo_url':params["git"], 'env' : env,'port': port}
        
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
                output =deploy_service.run_playbook('./templates/ansible/flask_deploy.yml')
                print(output)

            elif params["app_type"]=="node":

                # deploy a node app
                output =deploy_service.run_playbook('./templates/ansible/node_deploy.yml')
                print(output)

            else:
                raise Exception("Invalid App Type")
            
            if(output==0):
                return (f"Successfully Deployed the Application on instance at http://{public_ip}:{port} ")
            else:
                raise Exception("Failed to Deploy the Application")





