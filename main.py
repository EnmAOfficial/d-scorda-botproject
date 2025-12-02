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
        print("[BOOT] Slash komutlar Discord ile senkronize edildi.")


intents = discord.Intents.default()
intents.message_content = True

bot = MyBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"[BOOT] Bot giriş yaptı: {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_message(message: discord.Message):
    # Kendi mesajlarına cevap verme
    if message.author.bot:
        return

    channel = message.channel

    # AI bu kanalda cevap vermeye uygun mu?
    if is_ai_allowed_in_channel(channel):
        try:
            await channel.typing()
            answer = ask_gpt(message.content)
            if len(answer) <= 2000:
                await channel.send(answer)
            else:
                for i in range(0, len(answer), 2000):
                    await channel.send(answer[i:i+2000])
        except Exception as e:
            print(f"[ERROR] Auto-AI cevabında hata: {e}")

    # Eğer ileride prefixli komutlar kullanırsan diye:
    await bot.process_commands(message)


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ DISCORD_TOKEN tanımlı değil.")
    else:
        bot.run(DISCORD_TOKEN)
