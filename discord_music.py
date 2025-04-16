import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import yt_dlp as youtube_dl

# 環境変数の読み込み
load_dotenv()

# 環境変数からBotのアクセストークンを取得
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN 環境変数が設定されていません")

# 必要なインテントを設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を取得するためのインテントを有効化

# Botの設定
bot = commands.Bot(command_prefix="!", intents=intents)

# 起動時に動作する処理
@bot.event
async def on_ready():
    print('ログインしました')

# YouTube音楽再生コマンド
@bot.command()
async def play(ctx, url):
    # ボイスチャンネルに接続
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        try:
            voice_client = await channel.connect()
        except discord.ClientException:
            voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    else:
        await ctx.send("ボイスチャンネルに参加してください。")
        return

    # YouTube音源を取得
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']
    except Exception as e:
        await ctx.send("音源の取得に失敗しました。")
        print(f"エラー: {e}")
        return

    # 音楽を再生
    try:
        voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('再生終了:', e))
        await ctx.send(f"再生中: {info['title']}")
    except Exception as e:
        await ctx.send("音楽の再生に失敗しました。")
        print(f"エラー: {e}")

# Botの起動
bot.run(TOKEN)