# Author: David Kuda
# Creation Date: 1. October 2021
#
# Description:
#
# Interacts with the GitLab api to create new variables
# that can be used in gitlab ci.
#
# Documentation:
#
# https://docs.gitlab.com/ee/api/project_level_variables.html
#

import os
import configparser
from pprint import pprint

import requests


class GitLabClient:
    def __init__(self, gitlab_access_token, api_base_url) -> None:
        self.headers = {
            'PRIVATE-TOKEN': gitlab_access_token
        }
        self.api_base_url = api_base_url

    def get(self, api_endpoint: str):
        # Two examples:
        # projects = gitlab_client.get('/projects')
        # groups = gitlab_client.get('/groups')

        url = self.api_base_url + api_endpoint
        return requests.get(url=url, headers=self.headers).json()

    def post(self, api_endpoint: str, body):
        url = self.api_base_url + api_endpoint
        print(url)
        return requests.post(url=url,
                             headers=self.headers,
                             json=body).json()

    def put(self, api_endpoint: str, body):
        url = self.api_base_url + api_endpoint
        return requests.put(url=url,
                            headers=self.headers,
                            json=body).json()


class GitLabProjectVarClient(GitLabClient):
    def __init__(self, gitlab_access_token, api_base_url, project_num) -> None:
        super().__init__(gitlab_access_token, api_base_url)
        self.project_num = project_num

    def get_project_vars(self):
        endpoint = f'/projects/{self.project_num}/variables'
        return self.get(endpoint)

    def create_project_variable(self, var_key: str, var_value: str):
        url = f'/projects/{self.project_num}/variables'
        var_key = var_key.upper()

        post_body = {
            "variable_type": "env_var",
            "key": var_key,
            "value": var_value,
            "protected": True,
            "masked": False,
            "environment_scope": "*"
        }

        return self.post(url, post_body)

    def update_project_variable(self, var_key: str, var_value: str):
        var_key = var_key.upper()
        endpoint = f'/projects/{self.project_num}/variables/{var_key}'

        body = {
            "variable_type": "env_var",
            "key": var_key,
            "value": var_value,
            "protected": True,
            "masked": False,
            "environment_scope": "*"
        }

        return self.put(endpoint, body)


def main():
    A = 464
    B = 466
    C = 473

    PROJECT_NUMS = [A, B, C]

    # for project_num in PROJECT_NUMS:
        # set_vars_of_project(project_num)
    set_vars_of_project(C)


def set_vars_of_project(project_num):
    GITLAB_ACCESS_TOKEN = os.environ.get('GITLAB_PERSONAL_API_TOKEN')

    gitlab_project_var_client = GitLabProjectVarClient(
        gitlab_access_token=GITLAB_ACCESS_TOKEN,
        api_base_url='https://gitlab.alexanderthamm.com/api/v4',
        project_num=project_num
    )

    existing_variables = gitlab_project_var_client.get_project_vars()
    existing_var_keys = [v['key'] for v in existing_variables]

    vars = {
        "Data": "Dave",
        "Dater": "Daver",
        "Daterr": "Daverr"
    }

    for var_key, var_value in vars.items():
        var_key = var_key.upper()
        
        is_taken = check_if_var_is_taken(existing_var_keys, var_key)

        if not is_taken:
            response = gitlab_project_var_client.create_project_variable(
                var_key, var_value)
        else:
            response = gitlab_project_var_client.update_project_variable(
                var_key, var_value)

        print(f'Set the variable "{var_key}".')


def check_if_var_is_taken(existing_vars: list, var_key: str):
    if var_key in existing_vars:
        return True


if __name__ == '__main__':
    main()
