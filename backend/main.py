from version_control.github_client import GitHubClient

client = GitHubClient(
    token="",
    repo_full_name="Tarekun/aigile",
    # base_url="",
)
print(client.get_open_issues())
