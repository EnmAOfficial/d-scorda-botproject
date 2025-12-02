import base64
import httpx
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # Örn: EnmAOfficial/d-scorda-botproject
KB_FILE_PATH = "ai/knowledge_base.txt"

API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{KB_FILE_PATH}"


async def github_add_line(new_line: str):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    async with httpx.AsyncClient() as client:
        # Mevcut KB dosyasını çek
        response = await client.get(API_URL, headers=headers)
        data = response.json()

        sha = data["sha"]
        old_content = base64.b64decode(data["content"]).decode("utf-8")

        new_content = old_content + "\n" + new_line.strip()
        encoded = base64.b64encode(new_content.encode()).decode()

        payload = {
            "message": "AI KB Updated",
            "content": encoded,
            "sha": sha
        }

        await client.put(API_URL, headers=headers, json=payload)
