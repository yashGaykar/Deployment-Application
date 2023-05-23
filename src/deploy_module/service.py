"""DEPLOYMENT SERVICE  FILE"""


import os
import time
import shutil
import base64

import subprocess

from ..onboard_module.models import AWSAccount

from ansible import context
from ansible.module_utils.common.collections import ImmutableDict
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.executor.playbook_executor import PlaybookExecutor

from .constants import INSTANCE_AMI, AWS_REGION,INSTANCE_TYPE


class RunPlaybookService:
    """RUN PLAYBOOK SERVICE"""

    def __init__(self, inventory_file, project, key):
        """all the files for running playbook"""
        self.loader = DataLoader()
        self.inventory = InventoryManager(
            loader=self.loader, sources=[inventory_file.name])
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory)

        context.CLIARGS = ImmutableDict(
            connection='ssh',
            verbosity=2,
            remote_user='ubuntu',
            private_key_file=f'./private/keys_pairs/{key}.pem',
            become_method='sudo',
            check=False,
            syntax=None,
            start_at_task=None,
        )

        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory)

        self.passwords = {}

    def run_playbook(self, file):
        """RUN A PLAYBOOK"""

        # Create the playbook executor
        pbex = PlaybookExecutor(
            playbooks=[file],
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            passwords=self.passwords,
        )

        # Execute the playbook
        response = pbex.run()

        # Return a response
        return response


class DeployService:
    """DEPLOY SERVICE"""

    @staticmethod
    def execute_command(command, cwd, env={}):
        """EXCEUTE A COMMAND"""

        proc = subprocess.Popen(
            command, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, env=env)

        output = []
        proc.wait()

        while True:
            proc.poll()

            stdout, stderr = proc.communicate()
            if stdout:
                output.append(stdout.decode('utf-8'))
            if stderr:
                output.append(stderr.decode('utf-8'))

            if proc.returncode is not None:
                break
            time.sleep(0.01)

            if proc.returncode != 0:
                error = f"Failed to Execute command {command}"
                raise Exception(error)

        if output:
            print(output)
            return output
        return "No output"

    @staticmethod
    def terraform_env(port, project_name, account):
        """TERRAFORM ENVIRONMENT VARIABLES"""

        instance_key = (account.key_name).split(".")[0]
        access_key = base64.b64decode(account.access_key).decode()
        secret_key = base64.b64decode(account.secret_key).decode()

        env = {
            "TF_VAR_aws_region": AWS_REGION,
            "TF_VAR_aws_access_key": access_key,
            "TF_VAR_aws_secret_access_key": secret_key,
            "TF_VAR_app_port": port,
            "TF_VAR_instance_ami": INSTANCE_AMI,
            "TF_VAR_instance_key": instance_key,
            "TF_VAR_instance_type": INSTANCE_TYPE,
            "TF_VAR_project_name": project_name
        }
        return env

    @staticmethod
    def check_project_exists(project_name):
        """CHECKS IF THE PROJECT EXISTS"""
        infrastructure_exists = os.path.exists(f'./infras/{project_name}')
        return infrastructure_exists

    @staticmethod
    def delete_project_folder(project_name):
        """Deletes the infrastructure details folder """
        shutil.rmtree(f'./infras/{project_name}')
