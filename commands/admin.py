import discord
from discord import app_commands
from discord.ext import commands

from ai.state import (
    toggle_channel_ai,
    toggle_global_ai,
    is_channel_ai_active,
    is_global_ai_active
)

from config import ADMIN_ROLE_ID


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----------------------------------------------------
    # Rol yetkisi kontrolü
    # ----------------------------------------------------
    def has_admin_role(self, interaction: discord.Interaction) -> bool:
        role_ids = [r.id for r in interaction.user.roles]
        return ADMIN_ROLE_ID in role_ids

    # ============================================================
    # /ai-dur  → Bu kanalda AI kapat
    # ============================================================
    @app_commands.command(
        name="ai-dur",
        description="Bu kanalda yapay zekayı devre dışı bırakır."
    )
    async def ai_dur(self, interaction: discord.Interaction):

        if not self.has_admin_role(interaction):
            await interaction.response.send_message(
                "❌ Bu komutu kullanmaya yetkin yok.", ephemeral=True
            )
            return

        toggle_channel_ai(interaction.channel_id, False)

        await interaction.response.send_message(
            "🛑 AI **bu kanalda** devre dışı bırakıldı."
        )

    # ============================================================
    # /ai-basla → Bu kanalda AI aç
    # ============================================================
    @app_commands.command(
        name="ai-basla",
        description="Bu kanalda yapay zekayı aktif eder."
    )
    async def ai_basla(self, interaction: discord.Interaction):

        if not self.has_admin_role(interaction):
            await interaction.response.send_message(
                "❌ Bu komutu kullanmaya yetkin yok.", ephemeral=True
            )
            return

        toggle_channel_ai(interaction.channel_id, True)

        await interaction.response.send_message(
            "✅ AI **bu kanalda** aktif edildi."
        )

    # ============================================================
    # /ai-aktif → Global AI aç
    # ============================================================
    @app_commands.command(
        name="ai-aktif",
        description="Sunucudaki tüm kanallarda yapay zekayı aktif eder."
    )
    async def ai_aktif(self, interaction: discord.Interaction):

        if not self.has_admin_role(interaction):
            await interaction.response.send_message(
                "❌ Bu komutu kullanmaya yetkin yok.", ephemeral=True
            )
            return

        toggle_global_ai(True)

        await interaction.response.send_message(
            "🌍 AI **TÜM SUNUCUDA** aktif edildi."
        )

    # ============================================================
    # /ai-inaktif → Global AI kapat
    # ============================================================
    @app_commands.command(
        name="ai-inaktif",
        description="Sunucudaki tüm kanallarda yapay zekayı devre dışı bırakır."
    )
    async def ai_inaktif(self, interaction: discord.Interaction):

        if not self.has_admin_role(interaction):
            await interaction.response.send_message(
                "❌ Bu komutu kullanmaya yetkin yok.", ephemeral=True
            )
            return

        toggle_global_ai(False)

        await interaction.response.send_message(
            "🛑 AI **TÜM SUNUCUDA** devre dışı bırakıldı."
        )


# Slash komutlarını kayıt eden fonksiyon
def register_admin_commands(tree: app_commands.CommandTree):
    commands_obj = AdminCommands(tree.client)

    tree.add_command(commands_obj.ai_dur)
    tree.add_command(commands_obj.ai_basla)
    tree.add_command(commands_obj.ai_aktif)
    tree.add_command(commands_obj.ai_inaktif)
