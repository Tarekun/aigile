from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Issue:
    """Data structure representing an issue on version control system"""

    id: int
    title: str
    description: str
    state: str
    url: str
    # labels: Optional[List[str]] = None
    # assignees: Optional[List[str]] = None


class VCClient(ABC):
    """Abstract base class for version control system clients"""

    @abstractmethod
    def __init__(self, token: str, repo_full_name: str, base_url: str):
        """Initialize the client with connection details"""
        pass

    @abstractmethod
    def get_open_issues(self) -> List[Issue]:
        """Get all open issues for a repository"""
        pass

    @abstractmethod
    def add_comment_to_issue(self) -> bool:
        """Add a comment to an existing issue"""
        pass

    # @abstractmethod
    # def test_connection(self) -> bool:
    #     """Test if the client can connect to the VCS"""
    #     pass
