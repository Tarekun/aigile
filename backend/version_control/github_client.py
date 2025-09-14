from typing import List
from version_control.interface import VCClient, Issue, IssueFilter, empty_filters
from github import Github, GithubException, GithubObject
from typing import List, Optional, cast


def map_github_issues(github_issues) -> List[Issue]:
    return [
        Issue(
            id=issue.number,
            title=issue.title,
            description=issue.body or "",
            state=issue.state,
            url=issue.html_url,
            labels=[label.name for label in issue.labels],
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

    def get_issues(self, filters: IssueFilter = empty_filters) -> List[Issue]:
        try:
            state = filters.state if filters.state is not None else GithubObject.NotSet
            labels = (
                filters.labels if filters.labels is not None else GithubObject.NotSet
            )

            github_repo = self.github_client.get_repo(self.repo_full_name)
            issues = github_repo.get_issues(state=state, labels=labels)
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

    def post_new_issue(self, issue: Issue):
        try:
            github_repo = self.github_client.get_repo(self.repo_full_name)
            github_repo.create_issue(
                title=issue.title, body=issue.description, labels=issue.labels
            )
        except GithubException as e:
            if e.status == 404:
                raise ValueError(f"Repository {self.repo_full_name} not found")
            elif e.status == 403:
                raise PermissionError("Insufficient permissions to create issue")
            else:
                raise ConnectionError(f"GitHub API error: {e}")
        except Exception as e:
            raise ConnectionError(f"Unexpected error: {e}")

    def post_comment_to_issue(self, issue: Issue, comment: str):
        try:
            if issue.id is None:
                raise ValueError(
                    f"Cannot comment issue with no id. Input issue was {issue}"
                )
            github_repo = self.github_client.get_repo(self.repo_full_name)
            github_issue = github_repo.get_issue(number=issue.id)
            github_issue.create_comment(comment)
        except GithubException as e:
            if e.status == 404:
                raise ValueError(f"Issue {issue.id} not found")
            elif e.status == 403:
                raise PermissionError("Insufficient permissions to comment on issue")
            else:
                raise ConnectionError(f"GitHub API error: {e}")
        except Exception as e:
            raise ConnectionError(f"Unexpected error: {e}")

    def get_repo_url(self) -> str:
        return f"https://{self.token}@github.com/{self.repo_full_name}.git"
