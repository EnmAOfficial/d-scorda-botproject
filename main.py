import discord
from discord.ext import commands
from config import DISCORD_TOKEN

from commands.admin import register_admin_commands
from ai.state import is_ai_allowed_in_channel
from ai.openai_client import ask_gpt


class MyBot(commands.Bot):
    async def setup_hook(self):
        # Slash komutları kaydet
        register_admin_commands(self.tree)
        await self.tree.sync()
        print("[BOOT] Slash komutları Discord ile senkronize edildi.")


intents = discord.Intents.default()
intents.message_content = True

bot = MyBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"[BOOT] Bot giriş yaptı: {bot.user} (ID: {bot.user.id})")


# =====================================================
# Mesaj dinleyici — AI otomatik cevap sistemi
# =====================================================
@bot.event
async def on_message(message: discord.Message):

    # Bot mesajlarını atla
    if message.author.bot:
        return

    channel = message.channel

    # AI bu kanalda çalışmalı mı?
    if is_ai_allowed_in_channel(channel.id):

        try:
            await channel.typing()
            answer = ask_gpt(message.content)

            # 2000 karakter limiti için parçalara böl
            if len(answer) <= 2000:
                await channel.send(answer)
            else:
                for i in range(0, len(answer), 2000):
                    await channel.send(answer[i:i + 2000])

        except Exception as e:
            print(f"[ERROR] Auto-AI cevabında hata: {e}")

    # Komutların çalışabilmesi için
    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
