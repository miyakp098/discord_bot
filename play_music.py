import asyncio
from typing import Optional

import discord
import yt_dlp as youtube_dl
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source: discord.AudioSource, data: dict, volume: float = 0.5):
        """
        YTDLSourceクラスの初期化。

        Args:
            source (discord.AudioSource): 音声ソース。
            data (dict): YouTubeから取得したデータ。
            volume (float, optional): 音量。デフォルトは1.0。
        """
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url: str, *, stream: bool = False) -> 'YTDLSource':
        """
        指定されたURLから音声ソースを生成します。

        Args:
            url (str): YouTubeのURL。
            stream (bool, optional): ストリーミングモードかどうか。デフォルトはFalse。

        Returns:
            YTDLSource: 生成された音声ソース。
        """
        data = await cls._extract_info(url, stream)

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        youtube_dl_source = cls(discord.FFmpegPCMAudio(filename, options='-vn'), data=data)
        return youtube_dl_source

    @staticmethod
    async def _extract_info(url: str, stream: bool) -> dict:
        """
        YouTubeから情報を抽出します。

        Args:
            url (str): YouTubeのURL。
            stream (bool): ストリーミングモードかどうか。

        Returns:
            dict: 抽出された情報。
        """
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        return data



