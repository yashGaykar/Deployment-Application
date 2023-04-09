import os
import time

from src.settings import *
import subprocess
import time


from ansible import context
from ansible.module_utils.common.collections import ImmutableDict
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.executor.playbook_executor import PlaybookExecutor


class RunPlaybookService:
    def __init__(self, inventory_file):

        # all the files for running playbook
        self.loader = DataLoader()
        self.inventory = InventoryManager(
            loader=self.loader, sources=[inventory_file.name])
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory)

        context.CLIARGS = ImmutableDict(
            connection='ssh',
            verbosity=2,
            remote_user='ubuntu',
            private_key_file=os.getcwd()+f'/{INSTANCE_KEY}.pem',
            become_method='sudo',
            check=False,
            syntax=None,
            start_at_task=None,
        )

        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory)

        self.passwords = {}

    def run_playbook(self, file):
        try:

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
            return (response)

        except Exception as e:
            raise Exception(e)


class DeployService:
    
    def create_instance(ec2):

        # create a instance
        instances = ec2.run_instances(
            ImageId=IMAGE_ID,
            MinCount=1,
            MaxCount=1,
            InstanceType=INSTANCE_TYPE,
            KeyName=INSTANCE_KEY,
        )

        instance_id = instances["Instances"][0]["InstanceId"]
        print(instance_id)

        # waits until instance is in ready state
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])

        time.sleep(10)

        return instance_id

    def execute_command(command, cwd, env={}):

        proc = subprocess.Popen(
            command, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd,env=env)

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
                raise Exception(f"Error while running command {command}")

        if(output):
            print (output)
            return output
        return("No output")

