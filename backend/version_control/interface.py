from abc import ABC, abstractmethod
from typing import List, Optional, cast
from dataclasses import dataclass, field
from logger import logger


@dataclass
class Issue:
    """Data structure representing an issue on version control system"""

    title: str
    description: str
    state: str
    url: Optional[str] = None
    id: Optional[int] = None
    labels: List[str] = field(default_factory=list)
    # labels: Optional[List[str]] = None
    # assignees: Optional[List[str]] = None


@dataclass
class IssueFilter:
    state: Optional[str]
    labels: Optional[List[str]]


empty_filters = IssueFilter(state=None, labels=None)
MAX_RETRIES = 5


class VCClient(ABC):
    """Abstract base class for version control system clients"""

    @abstractmethod
    def __init__(self, token: str, repo_full_name: str, base_url: str):
        """Initialize the client with connection details"""
        pass

    @abstractmethod
    def get_issues(self, filters: IssueFilter = empty_filters) -> List[Issue]:
        """Single API call to fetch issues. No error handling expected"""
        pass

    @abstractmethod
    def post_comment_to_issue(self, issue: Issue, comment: str):
        """POST API call to add a comment to an existing issue. No error handling expected"""
        pass

    @abstractmethod
    def post_new_issue(self, issue: Issue):
        """POST API call to create a new issue. No error handling expected"""
        pass

    def _retry_api_call(self, callable):
        tries = 0
        error = None
        while tries < MAX_RETRIES:
            try:
                return callable()
            except Exception as e:
                logger.debug(f"API problem encountered, retrying. Details: {e}")
                tries += 1
                error = e

        logger.error("Retry limit reached on API call")
        raise cast(Exception, error)

    def fetch_issues(self, filters: IssueFilter = empty_filters) -> List[Issue]:
        """Fetches issues on the version control system"""

        logger.debug(f"Pulling issues with filter: {filters}")
        return self._retry_api_call(lambda: self.get_issues(filters))

    def fetch_feature_requests(self) -> List[Issue]:
        return self._retry_api_call(
            lambda: self.fetch_issues(
                IssueFilter(state="open", labels=["feature-request"])
            )
        )

    def comment_issue(self, issue: Issue, comment: str):
        """Adds the provided string as a comment to the `issue`"""

        logger.debug(f"Leaving comment on issue #{issue.id}")
        self._retry_api_call(lambda: self.post_comment_to_issue(issue, comment))
        logger.debug(f"Comment created successfully")

    def create_issue(self, issue: Issue):
        """Creates a new issue to the version control system"""

        logger.debug(f"Creating new issue from object {issue}")
        self._retry_api_call(lambda: self.post_new_issue(issue))
        logger.debug(f"Issue created successfully")
