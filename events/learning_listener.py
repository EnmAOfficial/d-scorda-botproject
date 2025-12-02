import discord
from discord.ext import commands
from ai.kb_manager import save_to_kb
import os


class LearningListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.learning_channel_id = int(os.getenv("LEARNING_CHANNEL_ID", "0"))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        if message.channel.id != self.learning_channel_id:
            return

        text = message.content.strip()
        if not text:
            return

        # Otomatik KB öğrenme
        await save_to_kb(
            bot=self.bot,
            text=text,
            source="🤖 Otomatik Öğrenme Kanali",
            user=message.author,
            channel=message.channel
        )


async def setup(bot):
    await bot.add_cog(LearningListener(bot))
