"""Tests Deployment"""

import time
from builtins import classmethod, print, str
import os
import random

import pytest
import requests


from dotenv import load_dotenv
DOTENV_PATH = '.env'
load_dotenv(DOTENV_PATH)


class TestDeployApp:
    """Application Deployment Test"""

    @classmethod
    def setup_class(cls):
        """Variables to be used in Tests"""
        random_num = random.randint(999, 99999)
        cls.data = {
            "git": os.environ.get("GIT_HUB_LINK"),
            "app_type": os.environ.get("APP_TYPE"),
            "env": {
                "DATABASE_URI": os.environ.get("DATABASE_URI"),
                "JWT_SECRET_KEY": os.environ.get("SECRET_KEY")
            },
            "project_name": f"AVI{random_num}",
            "port": os.environ.get("PORT")
        }

        cls.deploy_url = "http://127.0.0.1:5000/api/deploy/deploy"

        cls.status_url = "http://127.0.0.1:5000/api/deploy/deploy_task_status"

        cls.clean_up_url = "http://127.0.0.1:5000/api/deploy/cleanup"

        cls.clean_up_status_url = "http://127.0.0.1:5000/api/deploy/clean_up_task_status"

    def test_app_type_missing(self):
        """APP_TYPE MISSING"""
        input_data = self.data.copy()
        input_data.pop("app_type")
        response = requests.post(self.deploy_url, json=input_data, timeout=10)
        assert response.status_code == 400
        assert "'app_type': ['Missing data for required field.']" in str(
            response.json())

    def test_app_type_invalid(self):
        """APP_TYPE INVALID"""
        input_data = self.data.copy()
        input_data["app_type"] = "h"
        response = requests.post(self.deploy_url, json=input_data, timeout=10)
        assert response.status_code == 400
        assert "'app_type': ['Invalid value.']" in str(response.json())

    def test_git_link_missing(self):
        """GIT_LINK MISSING"""
        input_data = self.data.copy()
        input_data.pop("git")
        response = requests.post(self.deploy_url, json=input_data, timeout=10)
        assert response.status_code == 400
        assert "'git': ['Missing data for required field.']" in str(
            response.json())

    def test_port_missing(self):
        """PORT MISSING"""
        input_data = self.data.copy()
        input_data.pop("port")
        response = requests.post(self.deploy_url, json=input_data, timeout=10)
        assert response.status_code == 400
        assert "'port': ['Missing data for required field.']" in str(
            response.json())

    def test_project_name_missing(self):
        """PROJECT NAME MISSING"""
        input_data = self.data.copy()
        input_data.pop("project_name")
        response = requests.post(self.deploy_url, json=input_data, timeout=10)
        assert response.status_code == 400
        assert "'project_name': ['Missing data for required field.']" in str(
            response.json())

    def test_deploy_success(self):
        """DEPLOY SUCCESSFULLY"""
        input_data = self.data.copy()
        response = requests.post(self.deploy_url, json=input_data, timeout=10)

        task_id = response.json()["id"]
        assert response.status_code == 200
        state = "PENDING"
        while state == "PENDING":
            status_response = requests.get(
                self.status_url, json={"id1": task_id}, timeout=10)
            print("Deployment in Process")
            state = status_response.json()["state"]
            time.sleep(20)
        assert status_response.status_code == 200
        assert 'Successfully Deployed the Application' in str(
            status_response.json()["status"])

    @pytest.mark.depends(on=['test_deploy_success'])
    def test_project_with_name_already_exists(self):
        """PROJECT ALREADY EXISTS"""
        input_data = self.data.copy()
        response = requests.post(self.deploy_url, json=input_data, timeout=10)
        assert response.status_code == 400
        assert response.json()=={'error': 'Project already Exists'}

    @pytest.mark.depends(on=['test_deploy_success'])
    def test_clean_up(self):
        """CLEAN THE INFRA STRUCTURE CREATED"""
        input_data = self.data.copy()
        response = requests.post(self.clean_up_url, json=input_data, timeout=10)

        task_id = response.json()["id"]
        assert response.status_code == 200
        state = "PENDING"
        while state == "PENDING":
            status_response = requests.get(
                self.clean_up_status_url, json={"id1": task_id}, timeout=10)
            print("Clean Up in Process")
            state = status_response.json()["state"]
            time.sleep(5)
        assert status_response.status_code == 200
        assert 'Successfully ' in str(
            status_response.json()["status"])
  
    @pytest.mark.depends(on=['test_clean_up'])
    def test_no_project_exist_to_clean_up(self):
        """PROJECT DOESN'T EXISTS"""
        input_data = self.data.copy()
        response = requests.post(self.clean_up_url, json=input_data, timeout=10)
        assert response.status_code == 400
        assert response.json()=={'error': 'Project does not Exists'}
        