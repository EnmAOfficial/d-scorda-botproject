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
    # ❗ Yetki Kontrolü – Sadece belirlenen rol kullanabilir
    # ----------------------------------------------------
    def has_admin_role(self, interaction: discord.Interaction) -> bool:
        role_ids = [r.id for r in interaction.user.roles]
        return ADMIN_ROLE_ID in role_ids

    # ====================================================
    # /ai-dur → Bu kanalda AI'yı durdur
    # ====================================================
    @app_commands.command(
        name="ai-dur",
        description="Bu kanalda yapay zekayı devre dışı bırakır."
    )
    async def ai_dur(self, interaction: discord.Interaction):

        # Yetki kontrolü
        if not self.has_admin_role(interaction):
            await interaction.response.send_message(
                "❌ Bu komutu kullanma yetkin yok.",
                ephemeral=True
            )
            return

        toggle_channel_ai(interaction.channel_id, False)

        await interaction.response.send_message(
            f"🛑 AI **bu kanalda** devre dışı bırakıldı.",
            ephemeral=False
        )

    # ====================================================
    # /ai-basla → Bu kanalda AI'yı başlat
    # ====================================================
    @app_commands.command(
        name="ai-basla",
        description="Bu kanalda yapay zekayı aktif eder."
    )
    async def ai_basla(self, interaction: discord.Interaction):

        if not self.has_admin_role(interaction):
            await interaction.response.send_message(
                "❌ Bu komutu kullanma yetkin yok.",
                ephemeral=True
            )
            return

        toggle_channel_ai(interaction.channel_id, True)

        await interaction.response.send_message(
            f"✅ AI **bu kanalda** aktif edildi.",
            ephemeral=False
        )

    # ====================================================
    # /ai-aktif → Global olarak tüm sunucuda AI açılır
    # ====================================================
    @app_commands.command(
        name="ai-aktif",
        description="Sunucudaki tüm kanallarda yapay zekayı aktif eder."
    )
    async def ai_aktif(self, interaction: discord.Interaction):

        if not self.has_admin_role(interaction):
            await interaction.response.send_message(
                "❌ Bu komutu kullanma yetkin yok.",
                ephemeral=True
            )
            return

        toggle_global_ai(True)

        await interaction.response.send_message(
            f"🌍 AI **TÜM SUNUCUDA** aktif edildi.",
            ephemeral=False
        )

    # ====================================================
    # /ai-inaktif → Global olarak tüm AI kapanır
    # ====================================================
    @app_commands.command(
        name="ai-inaktif",
        description="Sunucudaki tüm kanallarda yapay zekayı devre dışı bırakır."
    )
    async def ai_inaktif(self, interaction: discord.Interaction):

        if not self.has_admin_role(interaction):
            await interaction.response.send_message(
                "❌ Bu komutu kullanma yetkin yok.",
                ephemeral=True
            )
            return

        toggle_global_ai(False)

        await interaction.response.send_message(
            f"🛑 AI **TÜM SUNUCUDA** devre dışı bırakıldı.",
            ephemeral=False
        )


# ==========================================================
# Slash komutlarını bota kaydeden fonksiyon
# ==========================================================
def register_admin_commands(tree: app_commands.CommandTree):
    tree.add_command(AdminCommands(tree.client).ai_dur)
    tree.add_command(AdminCommands(tree.client).ai_basla)
    tree.add_command(AdminCommands(tree.client).ai_aktif)
    tree.add_command(AdminCommands(tree.client).ai_inaktif)
