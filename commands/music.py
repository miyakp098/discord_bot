from discord.ext import commands
from utils.youtube import get_youtube_audio
from utils.voice import connect_to_voice_channel

def setup_music_commands(bot):
    @bot.command()
    async def play(ctx, url):
        voice_client = await connect_to_voice_channel(ctx)
        if not voice_client:
            return

        # YouTube音源を取得
        audio_source, title = await get_youtube_audio(url)
        if not audio_source:
            await ctx.send("音源の取得に失敗しました。")
            return

        # 音楽を再生
        try:
            voice_client.play(audio_source, after=lambda e: print(f"再生終了: {e}" if e else "再生が完了しました。"))
            await ctx.send(f"再生中: {title}")
        except Exception as e:
            await ctx.send("音楽の再生に失敗しました。")
            print(f"エラー: {e}")