import os

from settings import *

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
        self.inventory = InventoryManager(loader=self.loader, sources=[inventory_file.name])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)


        context.CLIARGS = ImmutableDict(
            connection='ssh',
            verbosity=2,
            module_path=None,
            forks=100,
            become=None,
            remote_user='ubuntu',
            private_key_file=os.getcwd()+f'/{INSTANCE_KEY}.pem',
            become_method='sudo',
            common_args='-o StrictHostKeyChecking=no',
            become_user=None,
            host_key_checking=False,
            check=False,
            listhosts=None,
            listtasks=None,
            listtags=None,
            syntax=None,
            start_at_task=None,
            display=None
        )

        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

        self.passwords = {}

    def run_playbook(self,file):
        try:

            # Create the playbook executor
            playbook_executor = PlaybookExecutor(
                playbooks=[file],
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
            )

            # Execute the playbook
            response=playbook_executor.run()
            # Remove the temporary inventory file
            os.remove(self.inventory_file.name)
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
        
        instance_id=instances["Instances"][0]["InstanceId"]
        print(instance_id)

        # waits until instance is in ready state
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])

        return instance_id