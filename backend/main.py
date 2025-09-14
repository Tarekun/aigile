from version_control.interface import Issue, MergeRequest
from version_control.github_client import GitHubClient
from version_control.gitea_client import GiteaClient
from agent.utils import callable_client
from agent.actions import process_feature_request_all
from dotenv import load_dotenv
import os


load_dotenv()

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
    token=os.getenv("TOKEN") or "",
    repo_full_name="Tarekun/proof",
    base_url="https://iaisy.net:30003/api/v1",
)
issue = Issue(
    title="issue di prova",
    description="creato automaticamente",
    state="open",
    labels=[],
)
mr = MergeRequest(id=180, title="", description="", state="open")
# client.comment_issue(issue, "commento prova")
# client.create_issue(issue)
# print(client.get_mr_diff(mr))
# process_feature_request_all(client, llm)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("webhooks.tmp:app", host="0.0.0.0", port=10080, reload=True)
