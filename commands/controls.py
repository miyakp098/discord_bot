from discord.ext import commands


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