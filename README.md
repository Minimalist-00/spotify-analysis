# Spotify Playlist Analysis

Spotifyプレイリスト内の各アーティストの曲数を集計し、ランキング形式で表示するツール。

## セットアップ

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 環境変数

`.env` ファイルを作成し、以下を設定：

```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

## 使い方

```bash
source venv/bin/activate
python analyze_playlist.py
```

初回実行時はブラウザでSpotifyログインが求められます。
