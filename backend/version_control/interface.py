from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass, field


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


class VCClient(ABC):
    """Abstract base class for version control system clients"""

    @abstractmethod
    def __init__(self, token: str, repo_full_name: str, base_url: str):
        """Initialize the client with connection details"""
        pass

    @abstractmethod
    def fetch_issues(self, filters: IssueFilter = empty_filters) -> List[Issue]:
        """Get all open issues for a repository"""
        pass

    @abstractmethod
    def add_comment_to_issue(self, issue: Issue, comment: str):
        """Add a comment to an existing issue"""
        pass

    @abstractmethod
    def post_new_issue(self, issue: Issue):
        """Creates the provided issue on the version control system"""
        pass

    def fetch_feature_requests(self) -> List[Issue]:
        return self.fetch_issues(IssueFilter(state="open", labels=["feature-request"]))

    # @abstractmethod
    # def test_connection(self) -> bool:
    #     """Test if the client can connect to the VCS"""
    #     pass
