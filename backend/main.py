from version_control.interface import Issue
from version_control.github_client import GitHubClient
from version_control.gitea_client import GiteaClient
from agent.utils import callable_client
from agent.actions import process_feature_request_all


# llm = callable_client(
#     provider="ollama",
#     host="http://192.168.1.104:11434",
#     model="hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q6_K",
# )
# client = GitHubClient(
#     token="",
#     repo_full_name="Tarekun/aigile",
#     # base_url="",
# )
# process_feature_request_all(client, llm)


# create_tables()
# store_issue(
#     Issue(
#         id=1, title="prova", description="descrizione", url="", state="open", labels=[]
#     )
# )
# client = GitHubClient(
#     token="",
#     repo_full_name="Tarekun/aigile",
#     # base_url="",
# )
client = GiteaClient(
    token="",
    repo_full_name="Tarekun/proof",
    base_url="https://iaisy.net:30003/api/v1",
)
issue = Issue(
    title="issue di prova",
    description="creato automaticamente",
    state="open",
    labels=[],
)
# client.comment_issue(issue, "commento prova")
# client.create_issue(issue)
print(client.get_issues())
# process_feature_request_all(client, llm)
