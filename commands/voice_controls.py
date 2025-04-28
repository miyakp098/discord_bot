import discord
from utils.voice import connect_to_voice_channel, get_audio_source

def setup_control_commands(bot: discord.ext.commands.Bot) -> None:
    """
    音声制御コマンドを設定します。

    Args:
        bot (discord.ext.commands.Bot): DiscordのBotオブジェクト。

    Returns:
        None
    """
    @bot.command()
    async def pause(ctx: discord.ext.commands.Context) -> None:
        """
        再生中の音楽を一時停止します。

        Args:
            ctx (discord.ext.commands.Context): コマンドのコンテキスト。

        Returns:
            None
        """
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await ctx.send("音楽を一時停止しました。")
        else:
            await ctx.send("再生中の音楽がありません。")

    @bot.command()
    async def resume(ctx: discord.ext.commands.Context) -> None:
        """
        一時停止中の音楽を再開します。

        Args:
            ctx (discord.ext.commands.Context): コマンドのコンテキスト。

        Returns:
            None
        """
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await ctx.send("音楽を再開しました。")
        else:
            await ctx.send("一時停止中の音楽がありません。")

    @bot.command()
    async def stop(ctx: discord.ext.commands.Context) -> None:
        """
        再生中の音楽を停止します。

        Args:
            ctx (discord.ext.commands.Context): コマンドのコンテキスト。

        Returns:
            None
        """
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.send("音楽を停止しました。")
        else:
            await ctx.send("再生中の音楽がありません。")

    @bot.command()
    async def play(ctx: discord.ext.commands.Context, url: str) -> None:
        """
        指定されたURLの音楽を再生します。

        Args:
            ctx (discord.ext.commands.Context): コマンドのコンテキスト。
            url (str): 再生するYouTubeのURL。

        Returns:
            None
        """
        voice_client = await connect_to_voice_channel(ctx)
        if not voice_client:
            return

        audio_source, title = await get_audio_source(url)
        if not audio_source:
            await ctx.send("音源の取得に失敗しました。")
            return

        try:
            voice_client.play(audio_source, after=lambda e: print(f"再生終了: {e}" if e else "再生が完了しました。"))
            await ctx.send(f"再生中: {title}")
        except Exception as e:
            await ctx.send("音楽の再生に失敗しました。")
            print(f"エラー: {e}")