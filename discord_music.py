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

# グローバル変数
voice_client = None

# 起動時に動作する処理
@bot.event
async def on_ready():
    print('ログインしました')

# YouTube音楽再生コマンド
@bot.command()
async def play(ctx, url):
    global voice_client
    # ボイスチャンネルに接続
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        try:
            if voice_client is None or not voice_client.is_connected():
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

# 音楽の一時停止コマンド
@bot.command()
async def pause(ctx):
    global voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send("音楽を一時停止しました。")
    else:
        await ctx.send("再生中の音楽がありません。")

# 音楽の再開コマンド
@bot.command()
async def resume(ctx):
    global voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await ctx.send("音楽を再開しました。")
    else:
        await ctx.send("一時停止中の音楽がありません。")

# 音楽の停止コマンド
@bot.command()
async def stop(ctx):
    global voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("音楽を停止しました。")
    else:
        await ctx.send("再生中の音楽がありません。")
# MP3ファイルを再生するコマンド
@bot.command()
async def play_local(ctx, filename):
    global voice_client
    # ボイスチャンネルに接続
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        try:
            if voice_client is None or not voice_client.is_connected():
                voice_client = await channel.connect()
        except discord.ClientException:
            voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    else:
        await ctx.send("ボイスチャンネルに参加してください。")
        return

    # ファイルパスを確認
    file_path = os.path.join(os.getcwd(), filename)
    if not os.path.isfile(file_path):
        await ctx.send(f"ファイルが見つかりません: {filename}")
        return

    # 音楽を再生
    try:
        voice_client.play(discord.FFmpegPCMAudio(file_path), before_options="-buffer_size 64K", after=lambda e: print(f"再生終了: {e}"))
        await ctx.send(f"再生中: {filename}")
        print(f"ローカルファイルを再生中: {file_path}")
    except Exception as e:
        await ctx.send("音楽の再生に失敗しました。")
        print(f"エラー: {e}")
        
# Botの起動
bot.run(TOKEN)