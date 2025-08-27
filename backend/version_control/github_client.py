from typing import List
from version_control.interface import VCClient, Issue
from github import Github, GithubException, PaginatedList
from github.Issue import Issue as GithubIssue


def map_github_issues(github_issues) -> List[Issue]:
    return [
        Issue(
            id=issue.number,
            title=issue.title,
            description=issue.body or "",
            state=issue.state,
            url=issue.html_url,
            # labels=[label.name for label in issue.labels],
            # assignees=[assignee.login for assignee in issue.assignees],
        )
        for issue in github_issues
    ]


class GitHubClient(VCClient):
    def __init__(
        self,
        token: str,
        repo_full_name: str,
        base_url: str = "https://api.github.com",
    ):
        self.base_url = base_url
        self.token = token
        self.repo_full_name = repo_full_name
        self.github_client = Github(base_url=base_url, login_or_token=token)

    def get_open_issues(self) -> List[Issue]:
        try:
            github_repo = self.github_client.get_repo(self.repo_full_name)
            issues = github_repo.get_issues(state="open")

            return map_github_issues(issues)

        except GithubException as e:
            if e.status == 404:
                raise ValueError(f"Repository {self.repo_full_name} not found")
            elif e.status == 403:
                raise PermissionError("Insufficient permissions to access repository")
            else:
                raise ConnectionError(f"GitHub API error: {e}")
        except Exception as e:
            raise ConnectionError(f"Unexpected error: {e}")

    def add_comment_to_issue(self) -> bool:
        return False

    # def test_connection(self) -> bool:
    #     return False
