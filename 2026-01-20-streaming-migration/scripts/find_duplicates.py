#!/usr/bin/env python3
"""Find duplicate videos in a playlist."""

import argparse
import sys
from collections import defaultdict

from ytmusicapi import YTMusic

AUTH_FILE = "data/ytmusicapi-browser.json"


def main():
    parser = argparse.ArgumentParser(description="Find duplicate videos in a playlist")
    parser.add_argument("--playlist", "-p", required=True, help="Playlist ID")
    args = parser.parse_args()

    yt = YTMusic(AUTH_FILE)

    print(f"Fetching playlist {args.playlist}...")
    playlist = yt.get_playlist(args.playlist, limit=None)

    tracks = playlist.get("tracks", [])
    print(f"Found {len(tracks)} tracks")

    # Group by video ID
    by_video_id = defaultdict(list)
    for i, track in enumerate(tracks):
        video_id = track.get("videoId")
        if video_id:
            by_video_id[video_id].append({
                "index": i,
                "title": track.get("title", "Unknown"),
                "artist": track.get("artists", [{}])[0].get("name", "Unknown") if track.get("artists") else "Unknown",
                "setVideoId": track.get("setVideoId"),
            })

    # Find duplicates
    duplicates = {vid: entries for vid, entries in by_video_id.items() if len(entries) > 1}

    if not duplicates:
        print("\nNo duplicates found")
        return

    print()
    for video_id, entries in sorted(duplicates.items(), key=lambda x: -len(x[1])):
        print(f"[{len(entries)}x] {entries[0]['artist']} - {entries[0]['title']}")
        print(f"     https://youtube.com/watch?v={video_id}")
        for entry in entries:
            print(f"     #{entry['index']} setVideoId={entry['setVideoId']}")
        print()

    print(f"Found {len(duplicates)} videos with duplicates")
    print(f"Total duplicate entries: {sum(len(e) for e in duplicates.values()) - len(duplicates)}")


if __name__ == "__main__":
    main()
