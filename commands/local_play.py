import os
import discord
from utils.voice import connect_to_voice_channel

def setup_local_play_commands(bot):
    @bot.command()
    async def play_local(ctx, filename):
        voice_client = await connect_to_voice_channel(ctx)
        if not voice_client:
            return

        # ファイルパスを確認
        file_path = os.path.join(os.getcwd(), filename)
        if not os.path.isfile(file_path):
            await ctx.send(f"ファイルが見つかりません: {filename}")
            return

        # 音楽を再生
        try:
            voice_client.play(discord.FFmpegPCMAudio(file_path), after=lambda e: print(f"再生終了: {e}"))
            await ctx.send(f"再生中: {filename}")
        except Exception as e:
            await ctx.send("音楽の再生に失敗しました。")
            print(f"エラー: {e}")