import discord
from discord import app_commands
from discord.ext import commands

from config import ADMIN_ROLE_ID, AI_LOG_CHANNEL_ID
from utils.github_sync import append_to_github_kb


# =============================
#  SLASH KOMUT YETKİ KONTROLÜ
# =============================
def is_admin(interaction: discord.Interaction) -> bool:
    """Kullanıcının gerekli role sahip olup olmadığını kontrol eder."""
    if interaction.user is None:
        return False

    # Rol ID eşleşiyor mu?
    return any(role.id == ADMIN_ROLE_ID for role in interaction.user.roles)


# =============================
#  ADMIN KOMUTLARI CLASS
# =============================
class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -----------------------------
    # /ai-start – Ticket kanalında AI aktif eder
    # -----------------------------
    @app_commands.command(name="ai-basla", description="Bu kanalda AI yanıtlarını AKTİF eder.")
    async def ai_start(self, interaction: discord.Interaction):
        if not is_admin(interaction):
            await interaction.response.send_message("❌ Bu komutu kullanmaya yetkin yok.", ephemeral=True)
            return

        await interaction.response.send_message("✅ Bu kanalda AI aktif edildi.", ephemeral=True)

    # -----------------------------
    # /ai-stop – Ticket kanalında AI durdurur
    # -----------------------------
    @app_commands.command(name="ai-dur", description="Bu kanalda AI yanıtlarını DURDURUR.")
    async def ai_stop(self, interaction: discord.Interaction):
        if not is_admin(interaction):
            await interaction.response.send_message("❌ Bu komutu kullanmaya yetkin yok.", ephemeral=True)
            return

        await interaction.response.send_message("⛔ Bu kanalda AI durduruldu.", ephemeral=True)

    # -----------------------------
    # /ai-add – Manuel öğrenme komutu
    # -----------------------------
    @app_commands.command(name="ai-add", description="Yapay zekaya yeni bilgi ekler.")
    @app_commands.describe(text="Eklenecek bilgi")
    async def ai_add(self, interaction: discord.Interaction, text: str):
        if not is_admin(interaction):
            await interaction.response.send_message("❌ Bu komutu kullanmaya yetkin yok.", ephemeral=True)
            return

        # Github’a yaz
        append_to_github_kb(f"- {text}")

        # AI Log kanalına mesaj gönder
        log_channel = interaction.client.get_channel(AI_LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(f"📘 Yeni bilgi eklendi: **{text}**")

        await interaction.response.send_message("✅ Yeni bilgi başarıyla eklendi!", ephemeral=True)


# =============================
#  REGISTER FONKSİYONU
# =============================
def register_admin_commands(tree: app_commands.CommandTree):
    tree.add_command(AdminCommands(tree.client).ai_start)
    tree.add_command(AdminCommands(tree.client).ai_stop)
    tree.add_command(AdminCommands(tree.client).ai_add)
