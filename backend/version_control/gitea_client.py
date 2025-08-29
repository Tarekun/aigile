from typing import List
from version_control.interface import VCClient, Issue, IssueFilter
import requests
from requests.exceptions import RequestException


def map_gitea_issues(gitea_issues) -> List[Issue]:
    return [
        Issue(
            id=issue["id"],
            title=issue["title"],
            description=issue["body"] or "",
            state=issue["state"],
            url=issue["html_url"],
        )
        for issue in gitea_issues
    ]


class GiteaClient(VCClient):
    """
    Implementation of the integration with a Gitea server.
    """

    def __init__(
        self,
        token: str,
        repo_full_name: str,
        base_url: str = "https://gitea.com/api/v1",
    ):
        self.base_url = base_url
        self.token = token
        self.repo_full_name = repo_full_name
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/json",
        }

    def get_open_issues(self, filters: IssueFilter) -> List[Issue]:
        """API reference:
        https://gitea.com/api/swagger#/issue/issueListIssues
        """
        try:
            url = f"{self.base_url}/repos/{self.repo_full_name}/issues"
            params = {"state": filters.state, "labels": filters.label}

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            issues = response.json()
            return map_gitea_issues(issues)

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Repository {self.repo_full_name} not found")
            elif e.response.status_code == 403:
                raise PermissionError("Insufficient permissions to access repository")
            else:
                raise ConnectionError(f"Gitea API error: {e}")
        except RequestException as e:
            raise ConnectionError(f"Network error connecting to Gitea: {e}")
        except Exception as e:
            raise ConnectionError(f"Unexpected error: {e}")

    def add_comment_to_issue(self) -> bool:
        return False
