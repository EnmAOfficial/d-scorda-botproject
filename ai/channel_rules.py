import discord
from config import TICKET_PREFIXES, AI_MANAGEMENT_PREFIX


def is_ticket_channel(channel: discord.abc.GuildChannel) -> bool:
    """Ticket kanalı mı? -> isme göre kontrol."""
    name = channel.name.lower()
    for prefix in TICKET_PREFIXES:
        if name.startswith(prefix.lower()):
            return True
    return False


def is_ai_management_channel(channel: discord.abc.GuildChannel) -> bool:
    """Yönetim için kullanılan 'ai-' kanalı mı?"""
    return channel.name.lower().startswith(AI_MANAGEMENT_PREFIX.lower())
