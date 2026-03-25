import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client, filters
import yt_dlp
import os

# 🔑 CONFIG
API_ID = 27459131
API_HASH = "836a42a092e122d47e1957423f613ec8"
BOT_TOKEN = "8573490792:AAFlUC7zd0x3XuI91QQ4Rv1F2N1iVKf0wJc"

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🔥 START
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "🔥 BOT TIKTOK PRO 🔥\n\n"
        "🎬 /mp4 link\n"
        "🎵 /mp3 link"
    )

# 🎵 MP3
@app.on_message(filters.command("mp3"))
async def mp3(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usa: /mp3 link")

    url = message.command[1]
    await message.reply("⏳ Extrayendo audio...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.endswith((".mp3", ".m4a", ".webm")):
                await message.reply_audio(file)
                os.remove(file)
                return

    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# 🎬 MP4
@app.on_message(filters.command("mp4"))
async def mp4(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usa: /mp4 link")

    url = message.command[1]
    await message.reply("⏳ Descargando video...")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.%(ext)s',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.endswith((".mp4", ".mkv", ".webm")):
                await message.reply_video(file)
                os.remove(file)
                return

    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# 🚀 RUN
if __name__ == "__main__":
    print("🔥 Bot encendido...")
    app.run()
