import discord

# メッセージ受信時に動作する処理
async def handle_message(client, message, target_channel_id):
    print(message.content)  # 受信したメッセージをターミナルに表示

    # DMで受信した場合
    if isinstance(message.channel, discord.DMChannel):
        # サーバー内の特定のチャンネルを取得
        target_channel = client.get_channel(target_channel_id)
        if target_channel:
            # DMの内容を送信
            await target_channel.send(f"DMからのメッセージ: {message.author} さん: {message.content}")
        else:
            print("指定されたチャンネルが見つかりません")
    else:
        # サーバー内の通常のメッセージ処理
        if message.content == 'aaa':
            await message.channel.send('test')