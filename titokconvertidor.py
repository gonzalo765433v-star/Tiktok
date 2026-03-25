import asyncio

asyncio.set_event_loop(asyncio.new_event_loop())
from pyrogram import Client, filters
import yt_dlp
import os
from flask import Flask
import threading

# 🔑 CONFIG
API_ID = 27459131
API_HASH = "836a42a092e122d47e1957423f613ec8"
BOT_TOKEN = "8717238239:AAGMzMZ2U-7_dpOjOo6tio06Ka1Vs7JYyiw"

app = Client("tiktok_pro_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🌐 WEB FAKE (PARA RENDER)
web = Flask(__name__)

@web.route("/")
def home():
    return "🔥 Bot activo"

def run_web():
    web.run(host="0.0.0.0", port=10000)

# 🚀 START BOT
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "🔥 BOT TIKTOK PRO 🔥\n\n"
        "🎬 /mp4 link\n"
        "🎵 /mp3 link"
    )

# 🎬 MP4
@app.on_message(filters.command("mp4"))
async def mp4(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usa: /mp4 link")

    url = message.command[1]
    await message.reply("⏳ Descargando video...")

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.endswith(".mp4"):
                await message.reply_video(file)
                os.remove(file)
                break

    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# 🎵 MP3
@app.on_message(filters.command("mp3"))
async def mp3(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usa: /mp3 link")

    url = message.command[1]
    await message.reply("⏳ Extrayendo audio...")

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.endswith(".mp3"):
                await message.reply_audio(file)
                os.remove(file)
                break

    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# 🔥 INICIAR TODO
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    app.run()
