"""
Spotify TOP50プレイリスト自動作成スクリプト
全期間のよく聴いた曲TOP50からプレイリストを作成する
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# 発行したトークン（環境変数または直接指定）
# ※ ここにテストで使用したトークンを設定してください
TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN", "BQDF-smUdokL_I-aipy6UQ0A0Nx0wdYl8IaUdYYIM9X1OeP2ayrTXQ7C4r9Ao3azUISLjwp5SK7CWFBpBBfSe8yBB03jt87uR3d2x6ygZRDlwqrzYgbme7VAq5wi0rKt7f9SEhw2Z5Mu3jG3dvQZjfNO6N1xCObfgE_r49WAE0s2pNhPro4RRWqIPS9n9YhOwiu0BGK1EWjCks6Xd4Iyk-9vU88dM1XQOCp9Rf30IIQYqFOaHiQUsrkxE04cDi0eFylLdpzQSaUdpzm__cOsLRQbT18VnlpIUwQHCUlPuu1AO9PURJZzVkHc6GZVz1ewDtYbUv4j")
LIMIT = 50


def fetch_web_api(endpoint, method="GET", body=None):
    url = f"https://api.spotify.com/{endpoint}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    if method == "GET":
        res = requests.get(url, headers=headers)
    elif method == "POST":
        res = requests.post(url, headers=headers, json=body)
    else:
        raise ValueError("Unsupported method")
        
    res.raise_for_status()
    return res.json()


def main():
    print("  ユーザー情報を取得中...")
    user_data = fetch_web_api("v1/me")
    user_id = user_data["id"]
    print(f"\n  ユーザー: {user_data.get('display_name', user_id)}")

    # TOP50トラック取得
    print(f"  期間: 全期間 (long_term)")
    print(f"  TOP{LIMIT}を取得中...\n")

    top_data = fetch_web_api(f"v1/me/top/tracks?time_range=long_term&limit={LIMIT}")
    tracks = top_data.get("items", [])
    if not tracks:
        print("  トップトラックが見つかりませんでした。")
        return

    # ランキング表示
    print(f"{'='*50}")
    print(f"  あなたのTOP{len(tracks)}（全期間）")
    print(f"{'='*50}\n")

    track_uris = []
    for i, track in enumerate(tracks, 1):
        artists = ", ".join(a["name"] for a in track["artists"])
        print(f"  {i}. {track['name']} - {artists}")
        track_uris.append(track["uri"])

    # プレイリスト作成
    playlist_name = "My All-Time TOP50 (API Version)"
    playlist_data = fetch_web_api(
        f"v1/users/{user_id}/playlists",
        method="POST",
        body={
            "name": playlist_name,
            "description": "全期間のよく聴いた曲TOP50（自動生成）",
            "public": False
        }
    )
    playlist_id = playlist_data["id"]

    # トラック追加
    fetch_web_api(
        f"v1/playlists/{playlist_id}/tracks",
        method="POST",
        body={"uris": track_uris}
    )

    print(f"\n{'='*50}")
    print(f"  ✅ プレイリスト「{playlist_name}」を作成しました！")
    print(f"  🔗 {playlist_data['external_urls']['spotify']}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
