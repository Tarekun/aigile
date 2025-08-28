from version_control.github_client import GitHubClient
from llm_api.tmp import callable_client

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
with open("./llm_api/prompts/feature_request.txt", "r", encoding="utf-8") as f:
    feature_request_prompt = f.read()

print(client.fetch_feature_requests())
for r in client.fetch_feature_requests():
    args = {"title": r.title, "description": r.description, "epics": []}
    print(llm(feature_request_prompt, args))
