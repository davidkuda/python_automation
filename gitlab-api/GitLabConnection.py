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

from pprint import pprint

import requests

from custom_exceptions import UnsuccessfulAuthentication


class GitLabConnection:
    def __init__(self, gitlab_access_token, api_base_url) -> None:
        self.gitlab_access_token = gitlab_access_token
        self.headers = {
            'PRIVATE-TOKEN': gitlab_access_token
        }
        self.api_base_url = api_base_url
        self.check_authentication()

    def check_authentication(self):
        response = self.get('/version')
        if response.get('error') == 'invalid_token':
            print(response.get('error_description'))
            raise UnsuccessfulAuthentication(response.get('error_description'))
        else:
            return True
        

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

    def list_groups(self):
        groups = self.get('/groups')
        group_names_and_id = []
        # pprint(groups[0].keys())
        for group in groups:
            group_names_and_id.append({
                    "group_id": group.get('id'),
                    "group_name": group.get('name')
                })
        pprint(group_names_and_id)

    def list_projects_of_group(self, group_num):
        projects_of_group = self.get(f'/groups/{group_num}/projects?per_page=100')
        print(len(projects_of_group))
        project_names_and_ids = []
        for project in projects_of_group:
            project_names_and_ids.append({
                "project_id": project.get('id'),
                "project_name": project.get('name')
            })
        pprint(project_names_and_ids)

    def search_group(self, name: str):
        # Does not work, API has no search scope for group.
        response = self.get(f'/search?scope=groups&search={name}')
        pprint(response)

    def search_project(self, name: str):
        response = self.get(f'/search?scope=projects&search={name}')
        pprint(response)

    def get_project_variables_object(self, project_num: int):
        return GitLabProjectVariables(
            self.gitlab_access_token,
            self.api_base_url,
            project_num
        )


class GitLabProjectVariables(GitLabConnection):
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

    def set_project_variables(self, variables: dict):

        for var_key, var_value in variables.items():
            var_key = var_key.upper()
            
            is_taken = self.check_if_var_is_taken(var_key)

            if not is_taken:
                response = self.create_project_variable(
                    var_key, var_value)
            else:
                response = self.update_project_variable(
                    var_key, var_value)

            print(f'Setting the variable "{var_key}".')

    def check_if_var_is_taken(self, var_key: str):
        existing_variables = self.get_project_vars()
        existing_var_keys = [v['key'] for v in existing_variables]
        if var_key in existing_var_keys:
            return True


if __name__ == '__main__':
    pass
