import asyncio
from pyrogram import Client, filters
import yt_dlp
import os
from flask import Flask
import threading
import uuid

# 🔑 CONFIG
API_ID = 
API_HASH = ""
BOT_TOKEN = ""

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🌐 WEB PARA RENDER
web = Flask(__name__)

@web.route('/')
def home():
    return "🔥 Bot activo"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)

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

    file_id = str(uuid.uuid4())

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{file_id}.%(ext)s',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        file = f"{file_id}.mp3"
        if os.path.exists(file):
            await message.reply_audio(file)
            os.remove(file)

    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# 🎬 MP4
@app.on_message(filters.command("mp4"))
async def mp4(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usa: /mp4 link")

    url = message.command[1]
    await message.reply("⏳ Descargando video...")

    file_id = str(uuid.uuid4())

    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{file_id}.%(ext)s',
            'quiet': True,
            'merge_output_format': 'mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        file = f"{file_id}.mp4"
        if os.path.exists(file):
            await message.reply_video(file)
            os.remove(file)

    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# 🚀 RUN
if __name__ == "__main__":
    print("🔥 Bot encendido...")

    # 🌐 servidor web (Render keep alive)
    threading.Thread(target=run_web, daemon=True).start()

    # 🤖 iniciar bot correctamente (FIX asyncio error)
    app.start()
    print("✅ Bot iniciado correctamente")
    asyncio.get_event_loop().run_forever()
