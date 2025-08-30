from typing import List
from gitlab import Gitlab, GitlabAuthenticationError, GitlabGetError, GitlabCreateError
from gitlab.v4.objects import Project, ProjectIssue
from version_control.interface import VCClient, Issue, IssueFilter, empty_filters


def map_gitlab_issues(gitlab_issues: List[ProjectIssue]) -> List[Issue]:
    return[
         Issue(
            id=issue.iid,
            title=issue.title,
            description=issue.description or "",
            state=issue.state,
            url=issue.web_url,
            labels=[label for label in issue.labels],
        )
        for issue in gitlab_issues
    ]

class GitLabClient(VCClient):
    def __init__(self, token: str, repo_full_name: str, base_url: str = "https://gitlab.com"):
        self.base_url = base_url
        self.token = token
        self.repo_full_name = repo_full_name
        self.gitlab_client = Gitlab(url=self.base_url, private_token= self.token)

    def get_issues(self, filters: IssueFilter = empty_filters) -> List[Issue]:
        try:
            project = self.gitlab_client.projects.get(self.repo_full_name)

            params = {}
            if filters.state is not None:
                params["state"] = filters.state
            if filters.labels is not None:
                params["labels"] = filters.labels

            git_lab_issues = project.issues.list(**params, all= True)
            return map_gitlab_issues(git_lab_issues)
        
        except GitlabGetError as e:
            if e.response_code == 404:
                raise ValueError(f"Project {self.repo_full_name} not found")
            elif e.response_code == 403:
                raise PermissionError("Insufficient permissions to access project")
            else:
                raise ConnectionError(f"GitLab API error: {e}")
        except Exception as e:
            raise ConnectionError(f"Unexpected error while fetching issues: {e}") from e
    
    
    def post_new_issue(self, issue: Issue):
        try:    
            project = self.gitlab_client.projects.get(self.repo_full_name)

            data = {
                "name" : issue.title,
                "title" : issue.title,
                "description" : issue.description
            }

            if issue.labels is not None:
                data["labels"] = ",".join(issue.labels)

            project.issues.create(data)

        except GitlabCreateError as e:
            if e.response_code == 404:
                raise ValueError(f"Project {self.repo_full_name} not found")
            elif e.response_code == 403:
                raise PermissionError("Insufficient permissions to create issue")
            else:
                raise ConnectionError(f"GitLab API error: {e}")
        except Exception as e:
            raise ConnectionError(f"Unexpected error while creating issue: {e}") from e
        

    
    def post_comment_to_issue(self, issue: Issue, comment: str):
        try:
            if issue.id is None:
                raise ValueError(f"Cannot comment on issue with no id. Input issue was {issue}")

            project = self.gitlab_client.projects.get(self.repo_full_name)
            git_lab_issue = project.issues.get(issue.id)

            git_lab_issue.notes.create({"body": comment})
        except GitlabGetError as e:
            if e.response_code == 404:
                raise ValueError(f"Issue {issue.id} not found in project {self.repo_full_name}")
            elif e.response_code == 403:
                raise PermissionError("Insufficient permissions to read issue or comment")
            else:
                raise ConnectionError(f"GitLab API error: {e}")
        except Exception as e:
            raise ConnectionError(f"Unexpected error while commenting on issue: {e}") from e

        