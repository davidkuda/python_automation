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
from pprint import pprint

from GitLabConnection import GitLabConnection


def main():

    GITLAB_ACCESS_TOKEN = os.environ.get('GITLAB_PERSONAL_API_TOKEN')

    gitlab_connection = GitLabConnection(
        gitlab_access_token=GITLAB_ACCESS_TOKEN,
        api_base_url='https://gitlab.alexanderthamm.com/api/v4'
    )
    
    gitlab_connection.list_groups()
    gitlab_connection.list_projects_of_group(362)
    gitlab_connection.search_project('spill')

    project_1 = 464
    project_2 = 466
    project_3 = 473

    projects = [
        project_1,
        project_2,
        project_3    
    ]

    vars = {
        "Data": "Dave",
        "Dater": "Daver",
        "Daterr": "Daverr"
    }
    
    for project in projects:
        project_variables = gitlab_connection.get_project_variables_object(project)
        project_variables.set_project_variables(vars)
    

if __name__ == '__main__':
    main()
