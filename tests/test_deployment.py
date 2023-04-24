
import time
from builtins import classmethod, print, str
import pytest
import requests
import random


class TestDeployApp:

    @classmethod
    def setup_class(self):
        random_num=random.randint(999,99999)
        global data
        data={
            "git": "https://github.com/yashGaykar/nodejs_practice.git",
            "app_type": "node",
            "env": {
                "DATABASE_URI": "mongodb+srv://yashgaykar:Gaya%40193@cluster0.nj9yven.mongodb.net/?retryWrites=true&w=majority",
                "JWT_SECRET_KEY": "SecretKey"
            },
            "project_name": f"AVI{random_num}",
            "port": "3000"
        }


        global deploy_url
        deploy_url="http://127.0.0.1:5000/api/deploy/deploy"

        global status_url
        status_url="http://127.0.0.1:5000/api/deploy/taskstatus"

    
    def test_app_type_missing(self):
        dict=data.copy()
        dict.pop("app_type")
        response=requests.post(deploy_url,json=dict)
        assert response.status_code == 400

    def test_app_type_invalid(self):
        dict=data.copy()
        dict["app_type"]="h"
        response=requests.post(deploy_url,json=dict)
        assert response.status_code == 400

    def test_git_link_missing(self):
        dict=data.copy()
        dict.pop("git")
        response=requests.post(deploy_url,json=dict)
        assert response.status_code == 400
    
    def test_port_missing(self):
        dict=data.copy()
        dict.pop("port")
        response=requests.post(deploy_url,json=dict)
        assert response.status_code == 400

    def test_project_name_missing(self):
        dict=data.copy()
        dict.pop("project_name")
        response=requests.post(deploy_url,json=dict)
        assert response.status_code == 400


    def test_git_link_missing(self):
        dict=data.copy()
        dict.pop("git")
        response=requests.post(deploy_url,json=dict)
        assert response.status_code == 400


    def test_success(self):
        dict=data.copy()
        response=requests.post(deploy_url,json=dict)

        id=(response.json()["id"])
        assert response.status_code == 200
        state="PENDING"
        while(state=="PENDING"):
            
            response_2=requests.get(status_url,json={"id1":id})
            print(f"Deployment in Process")
            state=response_2.json()["state"]
            time.sleep(20)
        assert 'Successfully Deployed the Application' in str(response_2.json()["status"])

    
    def test_project_with_name_already_exists(self):
        dict=data.copy()
        dict["project_name"]="AVI"
        response=requests.post(deploy_url,json=dict)
        id=(response.json()["id"])
        print(id)
        assert response.status_code == 200
        state="PENDING"
        while(state=="PENDING"):
            time.sleep(2)
            response_2=requests.get(status_url,json={"id1":id})
            print(response_2.json())
            state=response_2.json()["state"]
        assert response_2.json()["state"]== 'FAILURE'
        assert 'Project already exists' in str(response_2.json()["status"])

    


        


    

        
        
