import discord

async def connect_to_voice_channel(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        try:
            voice_client = await channel.connect()
            return voice_client
        except discord.ClientException:
            return discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    else:
        await ctx.send("ボイスチャンネルに参加してください。")
        return None