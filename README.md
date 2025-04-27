## 必要なパッケージのインストール
以下のコマンドを実行して、必要なパッケージをインストールします:
```bash
sudo apt update
sudo apt install python3.12-venv ffmpeg
```

## 仮想環境の作成とアクティブ化
1. 仮想環境を作成します:
```bash
python3.12 -m venv .venv
```
2. 仮想環境をアクティブにします:
```bash
source .venv/bin/activate
```

## 必要なPythonパッケージのインストール
以下のコマンドを実行して、必要なPythonパッケージをインストールします:
```bash
pip install pytest discord python-dotenv yt-dlp PyNaCl
```

## ボットの起動
以下のコマンドでボットを起動します:
```bash
python bot.py
```

## ボットの終了
ターミナル内で以下のキーを押してボットを終了します:
```
Ctrl + C
```
