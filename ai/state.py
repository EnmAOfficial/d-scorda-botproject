# AI çalışma durumlarını hafızada tutan sistem

# Global AI (tüm sunucu)
GLOBAL_AI_ENABLED = True

# Kanal bazlı AI durumları
CHANNEL_AI = {}  # {channel_id: True/False}


def toggle_global_ai(status: bool):
    global GLOBAL_AI_ENABLED
    GLOBAL_AI_ENABLED = status


def toggle_channel_ai(channel_id: int, status: bool):
    CHANNEL_AI[channel_id] = status


def is_channel_ai_active(channel_id: int) -> bool:
    if channel_id in CHANNEL_AI:
        return CHANNEL_AI[channel_id]
    return True  # varsayılan açık


def is_global_ai_active() -> bool:
    return GLOBAL_AI_ENABLED


def is_ai_allowed_in_channel(channel_id: int) -> bool:
    return is_global_ai_active() and is_channel_ai_active(channel_id)
