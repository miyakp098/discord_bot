import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import yt_dlp as youtube_dl
from discord.ui import View, Button, Modal, TextInput
import logging

# ログの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot_network.log"),  # ログをファイルに記録
        logging.StreamHandler()  # コンソールにも出力
    ]
)

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
            'preferredquality': '64',
        }],
        'noplaylist': True,  # プレイリストを無効化
        'quiet': True,  # コンソール出力を抑制
        'source_address': '0.0.0.0',  # IPv4を使用
        'nocheckcertificate': True,  # SSL証明書のチェックを無効化
        'default_search': 'auto',  # URLが不完全な場合に自動検索
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
        voice_client.play(
            discord.FFmpegPCMAudio(
                url2,
                before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin -loglevel debug",
                options="-vn -bufsize 512k"
            ),
            after=lambda e: print(f"再生終了: {e}" if e else "再生が完了しました。")
        )
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
        voice_client.play(discord.FFmpegPCMAudio(file_path), after=lambda e: print(f"再生終了: {e}"))
        await ctx.send(f"再生中: {filename}")
        print(f"ローカルファイルを再生中: {file_path}")
    except Exception as e:
        await ctx.send("音楽の再生に失敗しました。")
        print(f"エラー: {e}")
        return

    # 埋め込みメッセージとボタンを作成
    embed = discord.Embed(title="音楽コントロール", description=f"現在再生中: {filename}", color=discord.Color.blue())
    view = View()

    # 再生ボタン
    play_button = Button(label="再生", style=discord.ButtonStyle.green)
    async def play_callback(interaction):
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("音楽を再開しました。", ephemeral=True)
        else:
            await interaction.response.send_message("再生中の音楽がありません。", ephemeral=True)
    play_button.callback = play_callback
    view.add_item(play_button)

    # 一時停止ボタン
    pause_button = Button(label="一時停止", style=discord.ButtonStyle.blurple)
    async def pause_callback(interaction):
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("音楽を一時停止しました。", ephemeral=True)
        else:
            await interaction.response.send_message("再生中の音楽がありません。", ephemeral=True)
    pause_button.callback = pause_callback
    view.add_item(pause_button)

    # 停止ボタン
    stop_button = Button(label="停止", style=discord.ButtonStyle.red)
    async def stop_callback(interaction):
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("音楽を停止しました。", ephemeral=True)
        else:
            await interaction.response.send_message("再生中の音楽がありません。", ephemeral=True)
    stop_button.callback = stop_callback
    view.add_item(stop_button)

    # 埋め込みメッセージを送信
    await ctx.send(embed=embed, view=view)

@bot.command()
async def music_control(ctx):
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

    # 埋め込みメッセージとボタンを作成
    embed = discord.Embed(title="音楽コントロール", description="URLを入力して再生ボタンを押してください。", color=discord.Color.blue())
    view = View()

    # 再生ボタン
    play_button = Button(label="再生", style=discord.ButtonStyle.green)

    async def play_callback(interaction):
        # モーダルを作成してURLを入力させる
        class URLModal(Modal):
            def __init__(self):
                super().__init__(title="音楽再生 URL 入力")
                self.url_input = TextInput(label="YouTube URL", placeholder="https://www.youtube.com/watch?v=example", required=True)
                self.add_item(self.url_input)

            async def on_submit(self, interaction):
                url = self.url_input.value
                await interaction.response.send_message(f"再生中: {url}", ephemeral=True)
                await play_url(ctx, url)  # URLを再生する関数を呼び出す

        modal = URLModal()
        await interaction.response.send_modal(modal)

    play_button.callback = play_callback
    view.add_item(play_button)

    # 一時停止ボタン
    pause_button = Button(label="一時停止", style=discord.ButtonStyle.blurple)

    async def pause_callback(interaction):
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("音楽を一時停止しました。", ephemeral=True)
        else:
            await interaction.response.send_message("再生中の音楽がありません。", ephemeral=True)

    pause_button.callback = pause_callback
    view.add_item(pause_button)

    # 停止ボタン
    stop_button = Button(label="停止", style=discord.ButtonStyle.red)

    async def stop_callback(interaction):
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("音楽を停止しました。", ephemeral=True)
        else:
            await interaction.response.send_message("再生中の音楽がありません。", ephemeral=True)

    stop_button.callback = stop_callback
    view.add_item(stop_button)

    # 埋め込みメッセージを送信
    await ctx.send(embed=embed, view=view)


async def play_url(ctx, url):
    global voice_client

    # YouTube音源を取得
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '64',
        }],
        'noplaylist': True,
        'quiet': True,
        'source_address': '0.0.0.0',
        'nocheckcertificate': True,
        'default_search': 'auto',
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']
            title = info.get('title', 'タイトル不明')
    except Exception as e:
        await ctx.send("音源の取得に失敗しました。")
        print(f"エラー: {e}")
        return

    # 音楽を再生
    try:
        voice_client.play(
            discord.FFmpegPCMAudio(
                url2,
                before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -loglevel debug",
                options="-vn"
            ),
            after=lambda e: print(f"再生終了: {e}" if e else "再生が完了しました。")
        )
        await ctx.send(f"再生中: {title}")
    except Exception as e:
        await ctx.send("音楽の再生に失敗しました。")
        print(f"エラー: {e}")


# Botの起動
bot.run(TOKEN)