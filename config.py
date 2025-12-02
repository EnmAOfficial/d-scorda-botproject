import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Bu rol Slash komutlarını kontrol eder
ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID", "0"))
