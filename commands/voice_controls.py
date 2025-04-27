import discord
from utils.youtube import get_youtube_audio
from utils.voice import connect_to_voice_channel

def setup_control_commands(bot):
    @bot.command()
    async def pause(ctx):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await ctx.send("音楽を一時停止しました。")
        else:
            await ctx.send("再生中の音楽がありません。")

    @bot.command()
    async def resume(ctx):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await ctx.send("音楽を再開しました。")
        else:
            await ctx.send("一時停止中の音楽がありません。")

    @bot.command()
    async def stop(ctx):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.send("音楽を停止しました。")
        else:
            await ctx.send("再生中の音楽がありません。")

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