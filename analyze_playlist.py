"""
Spotifyプレイリスト アーティスト別曲数集計スクリプト
"""

import os
from collections import Counter
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

PLAYLIST_ID = "4LsnUc7eeubvt0LPpCuF3Z"


def get_playlist_tracks(sp, playlist_id):
    """プレイリストの全トラックを取得（100曲以上対応）"""
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results["items"])
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    return tracks


def main():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope="playlist-read-private playlist-read-collaborative",
            cache_path=".spotify_cache",
        )
    )

    # プレイリスト情報を取得
    playlist = sp.playlist(PLAYLIST_ID, fields="name")

    # 全トラック取得
    tracks = get_playlist_tracks(sp, PLAYLIST_ID)

    print(f"\n{'='*60}")
    print(f"  プレイリスト: {playlist['name']}")
    print(f"  合計曲数: {len(tracks)}")
    print(f"{'='*60}\n")

    # アーティストごとに曲数をカウント
    artist_counter = Counter()
    artist_tracks = {}  # アーティスト名 -> 曲名リスト

    for item in tracks:
        # APIバージョンによりキーが "track" または "item" の場合がある
        track = item.get("track") or item.get("item")
        if track is None or not isinstance(track, dict):
            continue

        track_name = track.get("name", "(不明)")
        artists = track.get("artists", [])
        # 1曲に複数アーティストがいる場合、それぞれカウント
        for artist in artists:
            name = artist["name"]
            artist_counter[name] += 1
            if name not in artist_tracks:
                artist_tracks[name] = []
            artist_tracks[name].append(track_name)

    # 曲数の多い順にソート
    sorted_artists = artist_counter.most_common()

    # 結果を表示（ランキング形式）
    for rank, (artist, count) in enumerate(sorted_artists, 1):
        print(f"  {rank}. {artist}: {count}曲")

    print(f"\n  アーティスト数合計: {len(sorted_artists)}")
    print()


if __name__ == "__main__":
    main()
