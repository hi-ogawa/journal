#!/usr/bin/env python3
"""Test if ytmusicapi can batch 'Add to library' for songs that support it."""

import json
from ytmusicapi import YTMusic

PLAYLIST_ID = "PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE"


def main():
    print("Initializing YTMusic...")
    yt = YTMusic("data/ytmusicapi-browser.json")

    # Test auth by checking library songs
    print("\nTesting auth: fetching library songs...")
    try:
        songs = yt.get_library_songs(limit=5)
        print(f"Library has songs: {len(songs)}")
        for s in songs[:3]:
            print(f"  - {s.get('title')}")
    except Exception as e:
        print(f"Auth error: {e}")
        return

    # Try get_album and add to library
    print("\nFetching album 'SOUL LADY'...")
    album = yt.get_album("MPREb_Tm5Mo0qAaI8")
    track = album["tracks"][2]  # SOUL LADY
    print(f"Track: {track['title']}, inLibrary: {track.get('inLibrary')}")
    print(f"feedbackTokens: {track.get('feedbackTokens')}")

    # Find a track NOT in library to test add
    for track in album["tracks"]:
        if not track.get("inLibrary"):
            tokens = track.get("feedbackTokens", {})
            if tokens.get("add"):
                print(f"\nFound track not in library: {track['title']}")
                print(f"Trying edit_song_library_status (add)...")
                try:
                    result = yt.edit_song_library_status([tokens["add"]])
                    print(f"Success! Result keys: {list(result.keys())}")
                except Exception as e:
                    print(f"Error: {e}")
                break
    else:
        print("\nAll tracks already in library or no add token available")


if __name__ == "__main__":
    main()
