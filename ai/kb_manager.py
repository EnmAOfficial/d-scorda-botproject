import os
from ai.github_sync import github_add_line

LOCAL_KB_PATH = "ai/knowledge_base.txt"
LOG_CHANNEL_ID = int(os.getenv("AI_LOG_CHANNEL_ID", "0"))


async def save_to_kb(bot, text: str, source: str, user=None, channel=None):
    text = text.strip()
    if not text:
        return False

    # 1) Lokal dosyaya yaz
    try:
        with open(LOCAL_KB_PATH, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except Exception as e:
        print("[KB-ERROR] Lokal yazma hatası:", e)

    # 2) GitHub KB güncelle
    try:
        await github_add_line(text)
    except Exception as e:
        print("[KB-ERROR] GitHub yazma hatası:", e)

    # 3) Log kanalına embed gönder
    try:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            import discord
            embed = discord.Embed(
                title="📘 Yeni Bilgi Öğrenildi",
                description=f"**Bilgi:**\n{text}",
                color=0x4CAF50
            )
            embed.add_field(name="Kaynak", value=source, inline=False)
            if user:
                embed.add_field(name="Ekleyen", value=user.mention, inline=False)
            if channel:
                embed.add_field(name="Kanal", value=channel.mention, inline=False)

            await log_channel.send(embed=embed)
    except Exception as e:
        print("[KB-ERROR] Log gönderilemedi:", e)

    return True
