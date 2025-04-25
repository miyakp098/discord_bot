import yt_dlp as youtube_dl
import discord

async def get_youtube_audio(url):
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
            audio_source = discord.FFmpegPCMAudio(
                url2,
                before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                options="-vn"
            )
            return audio_source, title
    except Exception as e:
        print(f"エラー: {e}")
        return None, None