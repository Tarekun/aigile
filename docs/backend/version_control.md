# Version Control Module

## Introduction

The version control module provides an interface for integrating with various version control systems (VCS) to enable web clients to interact with issue tracking systems. This module abstracts the differences between VCS providers, allowing the application to work with multiple platforms through a unified API.
The primary purpose of this module is to facilitate the retrieval and management of issues from version control systems.

## API Reference

### `Issue` Data Structure

The `Issue` class represents an issue or task within a version control system:

- `id`: int - Unique identifier for the issue
- `title`: str - Title or summary of the issue
- `description`: str - Detailed description of the issue
- `state`: str - Current state of the issue (e.g., "open", "closed")
- `url`: str - URL to view the issue online

### `VCClient` Interface

The `VCClient` abstract base class defines the interface that all version control system clients must implement:

#### Constructor

```python
def __init__(self, token: str, repo_full_name: str, base_url: str):
```

Parameters:

- `token`: str - Authentication token for accessing the VCS API
- `repo_full_name`: str - Full name of the repository (e.g., "owner/repo")
- `base_url`: str - Base URL for the VCS API endpoint

#### Methods

##### `get_open_issues()`

```python
def get_open_issues(self) -> List[Issue]:
```

Retrieves all open issues from the specified repository.

Returns:

- `List[Issue]` - A list of Issue objects representing open issues

Raises:

- `ValueError` - If the repository is not found
- `PermissionError` - If insufficient permissions to access the repository
- `ConnectionError` - For API connection or other unexpected errors

### Implementations

Currently, only one implementation is available:

#### GitHub Client (`GitHubClient`)

The `GitHubClient` class implements the `VCClient` interface for connecting to GitHub repositories. This implementation is based on the PyGithub library

Constructor:

```python
def __init__(
    self,
    token: str,
    repo_full_name: str,
    base_url: str = "https://api.github.com",
):
```

Parameters:

- `token`: str - GitHub personal access token
- `repo_full_name`: str - Full name of the GitHub repository (e.g., "owner/repo")
- `base_url`: str - GitHub API base URL (defaults to public GitHub API)
