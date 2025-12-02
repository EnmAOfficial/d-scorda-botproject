import base64
import requests
import os

GITHUB_REPO = os.getenv("GITHUB_REPO")  # ör: EnmAOfficial/d-scorda-botproject
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
KB_FILE_PATH = "ai/knowledge_base.txt"


def append_to_github_kb(new_line: str):
    """
    GPT öğrenme için Github'daki knowledge_base.txt dosyasına yeni satır ekler.
    """

    if not GITHUB_REPO or not GITHUB_TOKEN:
        print("[GITHUB] Repo veya Token ENV yok! Yazılamadı.")
        return False

    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{KB_FILE_PATH}"

    # Dosyanın mevcut halini çek
    response = requests.get(api_url, headers={
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    })

    if response.status_code != 200:
        print("[GITHUB] Mevcut dosya alınamadı:", response.text)
        return False

    data = response.json()
    file_sha = data["sha"]
    content = base64.b64decode(data["content"]).decode()

    # Yeni satır ekle
    updated = content + "\n" + new_line

    encoded_content = base64.b64encode(updated.encode()).decode()

    update_response = requests.put(api_url, json={
        "message": f"AI KB Update: {new_line[:30]}...",
        "content": encoded_content,
        "sha": file_sha
    }, headers={
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    })

    if update_response.status_code in [200, 201]:
        print("[GITHUB] KB başarıyla güncellendi.")
        return True

    print("[GITHUB] KB güncellenemedi:", update_response.text)
    return False
