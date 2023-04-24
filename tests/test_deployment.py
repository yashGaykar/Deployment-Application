
import time
from builtins import classmethod, print, str
import pytest
import requests
import random

from dotenv import load_dotenv
import os

dotenv_path = '.env'
load_dotenv(dotenv_path)

class TestDeployApp:

    @classmethod
    def setup_class(self):
        random_num=random.randint(999,99999)
        global data
        data={
            "git": os.environ.get("GIT_HUB_LINK")
,
            "app_type": os.environ.get("APP_TYPE"),
            "env": {
                "DATABASE_URI": os.environ.get("DATABASE_URI"),
                "JWT_SECRET_KEY": os.environ.get("SECRET_KEY")
            },
            "project_name": f"AVI{random_num}",
            "port": os.environ.get("PORT")
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
        assert "'app_type': ['Missing data for required field.']" in str(response.json())

    def test_app_type_invalid(self):
        dict=data.copy()
        dict["app_type"]="h"
        response=requests.post(deploy_url,json=dict)
        assert response.status_code == 400
        assert "'app_type': ['Invalid value.']" in str(response.json())

    def test_git_link_missing(self):
        dict=data.copy()
        dict.pop("git")
        response=requests.post(deploy_url,json=dict)
        assert response.status_code == 400
        assert "'git': ['Missing data for required field.']" in str(response.json())
    
    def test_port_missing(self):
        dict=data.copy()
        dict.pop("port")
        response=requests.post(deploy_url,json=dict)
        assert response.status_code == 400
        assert "'port': ['Missing data for required field.']" in str(response.json())

    def test_project_name_missing(self):
        dict=data.copy()
        dict.pop("project_name")
        response=requests.post(deploy_url,json=dict)
        assert response.status_code == 400
        assert "'project_name': ['Missing data for required field.']" in str(response.json())


    def test_success(self):
        dict=data.copy()
        response=requests.post(deploy_url,json=dict)

        id=(response.json()["id"])
        assert response.status_code == 200
        state="PENDING"
        while(state=="PENDING"):
            
            status_response=requests.get(status_url,json={"id1":id})
            print(f"Deployment in Process")
            state=status_response.json()["state"]
            time.sleep(20)
        assert status_response.status_code == 200
        assert 'Successfully Deployed the Application' in str(status_response.json()["status"])

    
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
            status_response=requests.get(status_url,json={"id1":id})
            print(status_response.json())
            state=status_response.json()["state"]
        assert status_response.status_code == 200
        assert status_response.json()["state"]== 'FAILURE'
        assert 'Project already exists' in str(status_response.json()["status"])