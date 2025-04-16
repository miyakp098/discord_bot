import discord
from dotenv import load_dotenv
import os
from message_handler import handle_message

# 環境変数の読み込み
load_dotenv()

# 環境変数からBotのアクセストークンを取得
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN 環境変数が設定されていません")
if not TARGET_CHANNEL_ID:
    raise ValueError("TARGET_CHANNEL_ID 環境変数が設定されていません")

# 必要なインテントを設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を取得するためのインテントを有効化

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

# 起動時に動作する処理
@client.event
async def on_ready():
    print('ログインしました')


@client.event
async def on_message(message):
    await handle_message(client, message, TARGET_CHANNEL_ID)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)