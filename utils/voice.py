from discord.ext.commands import Context
from utils.youtube_audio import YTDLSource
import discord

async def connect_to_voice_channel(ctx: Context) -> discord.VoiceClient:
    """
    ユーザーがいるボイスチャンネルに接続します。

    Args:
        ctx (Context): コマンドのコンテキスト。

    Returns:
        discord.VoiceClient: 接続されたボイスクライアント。
    """
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("ボイスチャンネルに参加していません。")
        return None

    channel = ctx.author.voice.channel
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.channel == channel:
        return voice_client

    if voice_client:
        await voice_client.disconnect()

    try:
        return await channel.connect()
    except Exception as e:
        await ctx.send("ボイスチャンネルへの接続に失敗しました。")
        print(f"エラー: {e}")
        return None
    
async def get_audio_source(url: str):
    """
    指定されたURLから音声ソースを取得します。

    Args:
        url (str): YouTubeのURL。

    Returns:
        tuple: 音声ソースとタイトル。
    """
    try:
        ytdl_source = await YTDLSource.from_url(url, stream=True)
        return ytdl_source, ytdl_source.title
    except Exception as e:
        print(f"音声ソースの取得に失敗しました: {e}")
        return None, None