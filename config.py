import os
from dotenv import load_dotenv

load_dotenv()

# ==========================
#  TOKEN & API KEYS
# ==========================
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ==========================
#  ROLE SETTINGS
# ==========================
# Slash komutlarını kullanabilecek rol
ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID", "0"))

# ==========================
#  CHANNEL SETTINGS
# ==========================
AI_LOG_CHANNEL_ID = int(os.getenv("AI_LOG_CHANNEL_ID", "0"))
LEARNING_CHANNEL_ID = int(os.getenv("LEARNING_CHANNEL_ID", "0"))

# ==========================
#  GITHUB SETTINGS (AI öğrenme senkronizasyonu için)
# ==========================
GITHUB_REPO = os.getenv("GITHUB_REPO")          # ör: EnmAOfficial/d-scorda-botproject
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")        # classic token (repo erişimi şart)
