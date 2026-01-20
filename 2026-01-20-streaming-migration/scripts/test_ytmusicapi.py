#!/usr/bin/env python3
"""Test if ytmusicapi can add videos to a regular YouTube playlist."""

from ytmusicapi import YTMusic

# Your playlist from the URL
PLAYLIST_ID = "PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE"

# Test video (from your fetch example)
TEST_VIDEO_ID = "9Yb51feoRYM"


def main():
    print("Initializing YTMusic...")
    yt = YTMusic("data/ytmusicapi-browser.json")

    # Fetch existing playlist to check for duplicates
    print(f"Fetching playlist {PLAYLIST_ID}...")
    playlist = yt.get_playlist(PLAYLIST_ID, limit=None)
    existing_ids = {track["videoId"] for track in playlist.get("tracks", [])}
    print(f"Playlist has {len(existing_ids)} existing tracks")

    # Check if test video already exists
    if TEST_VIDEO_ID in existing_ids:
        print(f"Video {TEST_VIDEO_ID} already in playlist, skipping")
        return

    print(f"Adding video {TEST_VIDEO_ID}...")
    try:
        result = yt.add_playlist_items(
            playlistId=PLAYLIST_ID,
            videoIds=[TEST_VIDEO_ID],
        )
        print("Success!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed: {e}")


if __name__ == "__main__":
    main()
