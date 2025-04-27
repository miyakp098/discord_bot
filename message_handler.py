import discord

async def handle_message(client: discord.Client, message: discord.Message, target_channel_id: int) -> None:
    """
    メッセージを処理し、必要に応じて特定のチャンネルに転送します。

    Args:
        client (discord.Client): Discordクライアントオブジェクト。
        message (discord.Message): 受信したメッセージオブジェクト。
        target_channel_id (int): 転送先のチャンネルID。

    Returns:
        None
    """
    print(message.content)  # 受信したメッセージをターミナルに表示

    if isinstance(message.channel, discord.DMChannel):
        target_channel = client.get_channel(target_channel_id)
        if target_channel:
            await target_channel.send(f"DMからのメッセージ: {message.author} さん: {message.content}")
        else:
            print("指定されたチャンネルが見つかりません")
    else:
        if message.content == 'aaa':
            await message.channel.send('test')