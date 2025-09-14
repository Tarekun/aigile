from typing import List
from version_control.interface import VCClient, Issue, IssueFilter, empty_filters
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

    def get_issues(self, filters: IssueFilter = empty_filters) -> List[Issue]:
        """API reference:
        https://gitea.com/api/swagger#/issue/issueListIssues
        """
        try:
            url = f"{self.base_url}/repos/{self.repo_full_name}/issues"
            params = {"state": filters.state, "labels": filters.labels}

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

    def post_comment_to_issue(self, issue: Issue, comment: str):
        if issue.id is None:
            raise ValueError("Issue object must have an 'id' set to post a comment.")

        try:
            url = f"{self.base_url}/repos/{self.repo_full_name}/issues/{issue.id}/comments"
            payload = {"body": comment}

            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(
                    f"Issue {issue.id} not found in repo {self.repo_full_name}"
                )
            elif e.response.status_code == 403:
                raise PermissionError("Insufficient permissions to post comment")
            else:
                raise ConnectionError(f"Gitea API error: {e}")
        except RequestException as e:
            raise ConnectionError(f"Network error connecting to Gitea: {e}")
        except Exception as e:
            raise ConnectionError(f"Unexpected error: {e}")

    def post_new_issue(self, issue: Issue):
        if not issue.title:
            raise ValueError("Issue must have a title to be created.")

        try:
            payload = {
                "title": issue.title,
                "body": issue.description,
                "labels": issue.labels,
            }
            response = requests.post(
                f"{self.base_url}/repos/{self.repo_full_name}/issues",
                headers=self.headers,
                json=payload,
            )

            response.raise_for_status()
            data = response.json()

            # Map API response back to your Issue dataclass
            # return Issue(
            #     title=data.get("title"),
            #     description=data.get("body", ""),
            #     state=data.get("state", ""),
            #     url=data.get("html_url"),
            #     id=data.get("number"),
            #     labels=[label.get("name") for label in data.get("labels", [])],
            # )

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                raise PermissionError("Insufficient permissions to create issue")
            else:
                raise ConnectionError(f"Gitea API error: {e}")
        except RequestException as e:
            raise ConnectionError(f"Network error connecting to Gitea: {e}")
        except Exception as e:
            raise ConnectionError(f"Unexpected error: {e}")
