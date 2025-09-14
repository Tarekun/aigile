from fastapi import FastAPI, Request, Header, HTTPException
from typing import Optional
import hmac
import hashlib

app = FastAPI()

# Optional: set your webhook secret from Gitea
WEBHOOK_SECRET = "mysecret"


def verify_signature(payload_body: bytes, signature: str) -> bool:
    """Verify X-Gitea-Signature using HMAC SHA256"""
    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = mac.hexdigest()
    return hmac.compare_digest(expected_signature, signature)


@app.post("/webhook/gitea/pr")
async def gitea_pr_webhook(
    request: Request,
    x_gitea_event: str = Header(None),
    x_gitea_signature: Optional[str] = Header(None),
):
    """
    Webhook endpoint for Gitea pull request events.
    """

    body = await request.body()

    # Verify signature if secret is set
    # if WEBHOOK_SECRET:
    #     if not x_gitea_signature or not verify_signature(body, x_gitea_signature):
    #         raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()

    if x_gitea_event != "pull_request":
        return {"status": "ignored", "reason": f"Unhandled event: {x_gitea_event}"}

    action = payload.get("action")
    pull_request = payload.get("pull_request", {})

    pr_id = pull_request.get("number")
    pr_title = pull_request.get("title")
    pr_state = pull_request.get("state")

    # 👉 Here you can add your business logic
    print(f"[Webhook] PR #{pr_id} '{pr_title}' action={action}, state={pr_state}")

    return {"status": "ok", "action": action, "pr_id": pr_id}
