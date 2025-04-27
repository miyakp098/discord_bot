import os
import discord
from utils.voice import connect_to_voice_channel

def setup_local_play_commands(bot: discord.ext.commands.Bot) -> None:
    """
    ローカルファイル再生コマンドを設定します。

    Args:
        bot (discord.ext.commands.Bot): DiscordのBotオブジェクト。

    Returns:
        None
    """
    @bot.command()
    async def play_local(ctx: discord.ext.commands.Context, filename: str) -> None:
        """
        指定されたローカルファイルを再生します。

        Args:
            ctx (discord.ext.commands.Context): コマンドのコンテキスト。
            filename (str): 再生するファイル名。

        Returns:
            None
        """
        voice_client = await connect_to_voice_channel(ctx)
        if not voice_client:
            return

        file_path = os.path.join(os.getcwd(), filename)
        if not os.path.isfile(file_path):
            await ctx.send(f"ファイルが見つかりません: {filename}")
            return

        try:
            voice_client.play(discord.FFmpegPCMAudio(file_path), after=lambda e: print(f"再生終了: {e}"))
            await ctx.send(f"再生中: {filename}")
        except Exception as e:
            await ctx.send("音楽の再生に失敗しました。")
            print(f"エラー: {e}")