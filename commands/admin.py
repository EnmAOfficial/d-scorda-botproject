import discord
from discord import app_commands
from discord.ext import commands
from config import STAFF_ROLE_ID, AI_LOG_CHANNEL_ID

# Kanal bazlı AI aktif/pasif tutma
CHANNEL_AI_STATE = {}  # {channel_id: True/False}

def is_staff(user: discord.Member) -> bool:
    """Kullanıcının staff rolü olup olmadığını kontrol eder."""
    return any(role.id == STAFF_ROLE_ID for role in user.roles)


def log_message(guild: discord.Guild, message: str):
    """AI log kanalına mesaj gönderir."""
    channel = guild.get_channel(AI_LOG_CHANNEL_ID)
    if channel:
        try:
            return channel.send(message)
        except:
            pass


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # /ai-dur — Sadece bu kanalda AI’yı kapat
    # =========================
    @app_commands.command(name="ai-dur", description="Bu kanalda AI cevaplarını durdur.")
    async def ai_dur(self, interaction: discord.Interaction):
        if not is_staff(interaction.user):
            return await interaction.response.send_message("❌ Bu komutu kullanmaya yetkin yok.", ephemeral=True)

        CHANNEL_AI_STATE[interaction.channel_id] = False

        await interaction.response.send_message("🛑 Bu kanalda AI devre dışı bırakıldı.")
        await log_message(interaction.guild, f"🔴 /ai-dur — {interaction.user} tarafından kapatıldı.")

    # =========================
    # /ai-calistir — Bu kanalda AI’yı aç
    # =========================
    @app_commands.command(name="ai-calistir", description="Bu kanalda AI cevaplarını tekrar açar.")
    async def ai_calistir(self, interaction: discord.Interaction):
        if not is_staff(interaction.user):
            return await interaction.response.send_message("❌ Bu komutu kullanmaya yetkin yok.", ephemeral=True)

        CHANNEL_AI_STATE[interaction.channel_id] = True

        await interaction.response.send_message("✅ Bu kanalda AI yeniden aktif.")
        await log_message(interaction.guild, f"🟢 /ai-calistir — {interaction.user} tarafından açıldı.")

    # =========================
    # /ai-restart — Botun AI hafızasını sıfırlar (kanal bazlı)
    # =========================
    @app_commands.command(name="ai-restart", description="Bu kanalda AI durumunu sıfırlar.")
    async def ai_restart(self, interaction: discord.Interaction):
        if not is_staff(interaction.user):
            return await interaction.response.send_message("❌ Bu komutu kullanmaya yetkin yok.", ephemeral=True)

        if interaction.channel_id in CHANNEL_AI_STATE:
            del CHANNEL_AI_STATE[interaction.channel_id]

        await interaction.response.send_message("♻️ Bu kanalda AI durumu sıfırlandı.")
        await log_message(interaction.guild, f"♻️ /ai-restart — {interaction.user} tarafından çalıştırıldı.")


# REGISTER FONKSİYONU (Render'ın aradığı)
def register_admin_commands(tree: app_commands.CommandTree):
    tree.add_command(AdminCommands.ai_dur)
    tree.add_command(AdminCommands.ai_calistir)
    tree.add_command(AdminCommands.ai_restart)
