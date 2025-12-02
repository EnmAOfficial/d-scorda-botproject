import discord
from discord import app_commands
from config import ADMIN_ROLE_IDS
from ai.channel_rules import is_ticket_channel
from ai.state import (
    set_global_active,
    is_global_active,
    set_channel_override,
    is_ai_allowed_in_channel,
)
# clear_channel_override istersen daha sonra da kullanırız


def _is_admin_user(user: discord.Member) -> bool:
    """Kullanıcının yetkili rollerden birine sahip olup olmadığını kontrol eder."""
    if not ADMIN_ROLE_IDS:
        # Hiç admin rolü tanımlanmadıysa, güvenlik açısından herkes admin sayılmasın istersen
        # ama şimdilik boşsa herkese açmak yerine kapalı tutmak mantıklı.
        return False

    user_role_ids = {r.id for r in user.roles}
    return not ADMIN_ROLE_IDS.isdisjoint(user_role_ids)


def register_admin_commands(tree: app_commands.CommandTree):
    @tree.command(name="ai-komutlar", description="AI ile ilgili yönetim komutlarının listesini gösterir.")
    async def ai_commands(interaction: discord.Interaction):
        if not _is_admin_user(interaction.user):
            return await interaction.response.send_message(
                "❌ Bu komutu kullanma yetkin yok.", ephemeral=True
            )

        text = (
            "**AI Yönetim Komutları**\n\n"
            "`/ai-aktif`   → Yapay zekayı sunucu genelinde yeniden aktif eder.\n"
            "`/ai-inaktif` → Yapay zekayı sunucu genelinde tamamen kapatır.\n"
            "`/ai-basla`   → Sadece bulunduğun ticket kanalında AI yanıtlarını açar.\n"
            "`/ai-dur`     → Sadece bulunduğun ticket kanalında AI yanıtlarını durdurur.\n"
        )

        await interaction.response.send_message(text, ephemeral=True)

    @tree.command(name="ai-aktif", description="Yapay zekayı sunucu genelinde tekrar aktif eder.")
    async def ai_aktif(interaction: discord.Interaction):
        if not _is_admin_user(interaction.user):
            return await interaction.response.send_message(
                "❌ Bu komutu kullanma yetkin yok.", ephemeral=True
            )

        set_global_active(True)
        await interaction.response.send_message(
            "✅ Yapay zeka **SUNUCU GENELİNDE AKTİF** edildi.", ephemeral=True
        )

    @tree.command(name="ai-inaktif", description="Yapay zekayı sunucu genelinde tamamen kapatır.")
    async def ai_inaktif(interaction: discord.Interaction):
        if not _is_admin_user(interaction.user):
            return await interaction.response.send_message(
                "❌ Bu komutu kullanma yetkin yok.", ephemeral=True
            )

        set_global_active(False)
        await interaction.response.send_message(
            "⛔ Yapay zeka **SUNUCU GENELİNDE İNAKTİF** edildi.", ephemeral=True
        )

    @tree.command(
        name="ai-dur",
        description="Sadece bulunduğun ticket kanalında AI yanıtlarını durdurur.",
    )
    async def ai_dur(interaction: discord.Interaction):
        if not _is_admin_user(interaction.user):
            return await interaction.response.send_message(
                "❌ Bu komutu kullanma yetkin yok.", ephemeral=True
            )

        channel = interaction.channel
        if not isinstance(channel, (discord.TextChannel, discord.Thread)):
            return await interaction.response.send_message(
                "Bu komut sadece metin kanallarında kullanılabilir.", ephemeral=True
            )

        if not is_ticket_channel(channel):
            return await interaction.response.send_message(
                "Bu komut sadece ticket kanallarında kullanılabilir.", ephemeral=True
            )

        set_channel_override(channel.id, False)
        await interaction.response.send_message(
            f"⛔ Bu kanalda AI yanıtları **DURDURULDU**. Diğer ticket kanalları etkilenmedi.",
            ephemeral=True,
        )

    @tree.command(
        name="ai-basla",
        description="Sadece bulunduğun ticket kanalında AI yanıtlarını başlatır.",
    )
    async def ai_basla(interaction: discord.Interaction):
        if not _is_admin_user(interaction.user):
            return await interaction.response.send_message(
                "❌ Bu komutu kullanma yetkin yok.", ephemeral=True
            )

        channel = interaction.channel
        if not isinstance(channel, (discord.TextChannel, discord.Thread)):
            return await interaction.response.send_message(
                "Bu komut sadece metin kanallarında kullanılabilir.", ephemeral=True
            )

        if not is_ticket_channel(channel):
            return await interaction.response.send_message(
                "Bu komut sadece ticket kanallarında kullanılabilir.", ephemeral=True
            )

        set_channel_override(channel.id, True)
        await interaction.response.send_message(
            "✅ Bu kanalda AI yanıtları **AKTİF** edildi (global ayar da açıksa).",
            ephemeral=True,
        )
