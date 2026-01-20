#!/usr/bin/env python3
"""Remove duplicate videos from a playlist, keeping the first occurrence."""

import argparse
import sys
from collections import defaultdict

from ytmusicapi import YTMusic

AUTH_FILE = "data/ytmusicapi-browser.json"


def check_auth(yt: YTMusic) -> bool:
    """Verify credentials by testing counterpart lookup on known video pair."""
    try:
        # Dirty Loops - Next to You: ATV (rT_isNWT4gQ) <-> OMV (rV9uCmlMQ1c)
        watch = yt.get_watch_playlist("rT_isNWT4gQ")
        counterpart = watch["tracks"][0].get("counterpart")
        return counterpart is not None and counterpart.get("videoId") == "rV9uCmlMQ1c"
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description="Remove duplicate videos from a playlist")
    parser.add_argument("--playlist", "-p", required=True, help="Playlist ID")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show what would be removed")
    parser.add_argument("--limit", "-l", type=int, help="Limit number of duplicates to remove")
    args = parser.parse_args()

    yt = YTMusic(AUTH_FILE)

    print("Checking credentials...")
    if not check_auth(yt):
        print("Error: Auth credentials are stale. Please refresh:")
        print("  1. Go to music.youtube.com (logged in)")
        print("  2. DevTools → Network → find any POST request")
        print("  3. Update data/ytmusicapi-browser.json")
        sys.exit(1)
    print("Auth OK")

    print(f"Fetching playlist {args.playlist}...")
    playlist = yt.get_playlist(args.playlist, limit=None)

    tracks = playlist.get("tracks", [])
    print(f"Found {len(tracks)} tracks")

    # Group by video ID
    by_video_id = defaultdict(list)
    for i, track in enumerate(tracks):
        video_id = track.get("videoId")
        set_video_id = track.get("setVideoId")
        if video_id and set_video_id:
            by_video_id[video_id].append({
                "index": i,
                "title": track.get("title", "Unknown"),
                "artist": track.get("artists", [{}])[0].get("name", "Unknown") if track.get("artists") else "Unknown",
                "videoId": video_id,
                "setVideoId": set_video_id,
            })

    # Collect duplicates to remove (keep first, remove rest)
    to_remove = []
    for video_id, entries in by_video_id.items():
        if len(entries) > 1:
            # Keep first (lowest index), remove the rest
            for entry in entries[1:]:
                to_remove.append(entry)

    if not to_remove:
        print("\nNo duplicates to remove")
        return

    if args.limit:
        to_remove = to_remove[:args.limit]

    print(f"\nDuplicates to remove: {len(to_remove)}")
    print(f"Sample:")
    for entry in to_remove[:5]:
        print(f"  #{entry['index']} {entry['artist']} - {entry['title']}")
    if len(to_remove) > 5:
        print(f"  ... and {len(to_remove) - 5} more")

    if args.dry_run:
        print(f"\n[DRY RUN] Would remove {len(to_remove)} duplicate entries")
        return

    # Remove duplicates
    print(f"\nRemoving duplicates...")
    batch_size = 50
    success = 0
    failed = 0

    for i in range(0, len(to_remove), batch_size):
        batch = to_remove[i:i + batch_size]
        try:
            yt.remove_playlist_items(args.playlist, batch)
            success += len(batch)
            print(f"  Batch {i // batch_size + 1}: {len(batch)} removed")
        except Exception as e:
            print(f"  Error: {e}")
            failed += len(batch)

    print(f"\nDone! Removed {success} duplicates ({failed} failed)")


if __name__ == "__main__":
    main()
