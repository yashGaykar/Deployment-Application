"""Tests Deployment"""

import time
from builtins import classmethod, print, str
import os
# import pytest
import random
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

        cls.status_url = "http://127.0.0.1:5000/api/deploy/taskstatus"

    def test_app_type_missing(self):
        """APP_TYPE MISSING"""
        input_data = self.data.copy()
        input_data.pop("app_type")
        response = requests.post(self.deploy_url, json=dict, timeout=10)
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

    def test_success(self):
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

    def test_project_with_name_already_exists(self):
        """PROJECT ALREADY EXISTS"""
        input_data = self.data.copy()
        input_data["project_name"] = "AVI"
        response = requests.post(self.deploy_url, json=input_data, timeout=10)
        task_id = response.json()["id"]
        print(id)
        assert response.status_code == 200
        state = "PENDING"
        while state == "PENDING":
            time.sleep(2)
            status_response = requests.get(
                self.status_url, json={"id1": task_id}, timeout=10)
            print(status_response.json())
            state = status_response.json()["state"]
        assert status_response.status_code == 200
        assert status_response.json()["state"] == 'FAILURE'
        assert 'Project already exists' in str(
            status_response.json()["status"])
