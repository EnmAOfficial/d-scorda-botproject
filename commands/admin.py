from discord import app_commands
from discord.ext import commands
import discord
import os
from ai.kb_manager import save_to_kb


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.admin_role_id = int(os.getenv("ADMIN_ROLE_ID"))

    # Yetki kontrolü
    def is_admin(self, interaction: discord.Interaction):
        admin_role = interaction.guild.get_role(self.admin_role_id)
        return admin_role in interaction.user.roles

    # /ai-add komutu
    @app_commands.command(
        name="ai-add",
        description="Yapay zekaya manuel olarak bilgi ekle"
    )
    @app_commands.describe(bilgi="Eklenecek bilgi metni")
    async def ai_add(self, interaction: discord.Interaction, bilgi: str):

        if not self.is_admin(interaction):
            return await interaction.response.send_message(
                "❌ Bu komutu kullanma yetkin yok.",
                ephemeral=True
            )

        await interaction.response.send_message("⏳ Bilgi ekleniyor...", ephemeral=True)

        await save_to_kb(
            bot=self.bot,
            text=bilgi,
            source="🔧 /ai-add komutu",
            user=interaction.user,
            channel=interaction.channel
        )

        await interaction.followup.send(
            "✅ Yeni bilgi başarıyla eklendi!",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Admin(bot))
