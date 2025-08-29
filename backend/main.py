from version_control.interface import Issue
from version_control.github_client import GitHubClient
from agent.utils import callable_client
from agent.actions import process_feature_request_all


llm = callable_client(
    provider="ollama",
    host="http://192.168.1.104:11434",
    model="hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q6_K",
)
client = GitHubClient(
    token="",
    repo_full_name="Tarekun/aigile",
    # base_url="",
)
process_feature_request_all(client, llm)
