import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN 環境変数が設定されていません")

# 必要なインテントを設定
intents = discord.Intents.default()
intents.message_content = True

# Botの設定
bot = commands.Bot(command_prefix="!", intents=intents)

# コマンドの読み込み
from commands.voice_controls import setup_control_commands

setup_control_commands(bot)

# 起動時の処理
@bot.event
async def on_ready():
    print('ログインしました')

# Botの起動
bot.run(TOKEN)