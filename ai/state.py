from typing import Dict
import discord

from config import GLOBAL_AI_DEFAULT_ACTIVE
from .channel_rules import is_ticket_channel, is_ai_management_channel

# Global AI durumu (tüm sunucu)
_global_ai_active: bool = GLOBAL_AI_DEFAULT_ACTIVE

# Kanal bazlı override:
# channel_id -> True (zorla açık), False (zorla kapalı)
_channel_overrides: Dict[int, bool] = {}


def set_global_active(active: bool):
    global _global_ai_active
    _global_ai_active = active
    print(f"[STATE] Global AI aktiflik: {active}")


def is_global_active() -> bool:
    return _global_ai_active


def set_channel_override(channel_id: int, active: bool):
    _channel_overrides[channel_id] = active
    print(f"[STATE] Kanal override set: {channel_id} -> {active}")


def clear_channel_override(channel_id: int):
    if channel_id in _channel_overrides:
        del _channel_overrides[channel_id]
        print(f"[STATE] Kanal override temizlendi: {channel_id}")


def get_channel_override(channel_id: int):
    return _channel_overrides.get(channel_id, None)


def is_ai_allowed_in_channel(channel: discord.abc.GuildChannel) -> bool:
    """
    Senin kurala göre:
      - Sadece ticket kanallarında otomatik cevap
      - 'ai-' kanallarında otomatik cevap YOK
      - Diğer kanallarda otomatik cevap YOK
      - Global kapalıysa hiçbir yerde çalışmaz
      - Kanal override varsa ona göre
    """
    if not _global_ai_active:
        return False

    # Yönetim "ai-" kanalları: otomatik cevap YOK
    if is_ai_management_channel(channel):
        return False

    # Ticket kanalı mı?
    base_allowed = is_ticket_channel(channel)

    override = get_channel_override(channel.id)
    if override is not None:
        return override

    return base_allowed
