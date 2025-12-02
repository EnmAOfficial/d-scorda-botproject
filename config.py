import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Birden fazla rol ID'si ekleyebilirsin (virgülle)
# Örnek: "123456789012345678,987654321098765432"
_raw_admin_roles = os.getenv("ADMIN_ROLE_IDS", "").strip()
if _raw_admin_roles:
    ADMIN_ROLE_IDS = {
        int(x.strip()) for x in _raw_admin_roles.split(",") if x.strip().isdigit()
    }
else:
    ADMIN_ROLE_IDS = set()

# Ticket kanalı algılamak için isim prefix'leri
# Örn: ticket-0001, ticket-oyuncu vs.
TICKET_PREFIXES = ("ticket-", "🎫┃ticket")

# Yönetim ekibi için "ai-" ile başlayan kanallar
AI_MANAGEMENT_PREFIX = "ai-"

# Bot açıldığında AI varsayılan global durumu (True = açık)
GLOBAL_AI_DEFAULT_ACTIVE = True

import os

AUTH_ROLE_IDS = [
    int(rid.strip()) for rid in os.getenv("AUTH_ROLE_IDS", "").split(",") if rid.strip().isdigit()
]
