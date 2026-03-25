from pyrogram import Client, filters
import yt_dlp
import os

# 🔑 TUS DATOS
API_ID = 27459131
API_HASH = "836a42a092e122d47e1957423f613ec8"
BOT_TOKEN = "8717238239:AAGMzMZ2U-7_dpOjOo6tio06Ka1Vs7JYyiw"

app = Client("tiktok_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🔥 START
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "🔥 BOT TIKTOK PRO 🔥\n\n"
        "🎬 /mp4 link → descargar video\n"
        "🎵 /mp3 link → descargar audio"
    )

# 🎬 MP4
@app.on_message(filters.command("mp4"))
async def mp4(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usa: /mp4 link")

    url = message.command[1]
    msg = await message.reply("⏳ Descargando video...")

    try:
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': 'video.mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await message.reply_video("video.mp4")
        os.remove("video.mp4")

        await msg.delete()

    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# 🎵 MP3 (audio real del video)
@app.on_message(filters.command("mp3"))
async def mp3(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usa: /mp3 link")

    url = message.command[1]
    msg = await message.reply("⏳ Extrayendo audio...")

    try:
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'audio.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.endswith((".mp3", ".m4a", ".webm")):
                await message.reply_audio(file)
                os.remove(file)
                break

        await msg.delete()

    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# 🚀 INICIO
if __name__ == "__main__":
    print("🔥 Bot encendido...")
    app.run()
