#!/usr/bin/env python3
"""Export non-library-able songs (OMV/UGC) to a fallback playlist.

These are songs that can't be added to the YT Music Artists tab.
"""

import argparse
import sys

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
    parser = argparse.ArgumentParser(description="Export non-library songs to fallback playlist")
    parser.add_argument("--source", "-s", required=True, help="Source playlist ID")
    parser.add_argument("--target", "-t", required=True, help="Target fallback playlist ID")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show what would be done")
    args = parser.parse_args()

    yt = YTMusic(AUTH_FILE)

    # Verify auth is valid
    print("Checking credentials...")
    if not check_auth(yt):
        print("Error: Auth credentials are stale. Please refresh:")
        print("  1. Go to music.youtube.com (logged in)")
        print("  2. DevTools → Network → find any POST request")
        print("  3. Update data/ytmusicapi-browser.json")
        sys.exit(1)
    print("Auth OK")

    # Fetch source playlist
    print(f"Fetching source playlist {args.source}...")
    source = yt.get_playlist(args.source, limit=None)
    tracks = source.get("tracks", [])
    print(f"Found {len(tracks)} tracks")

    # Collect non-ATV video IDs
    non_atv = []
    atv_count = 0

    for track in tracks:
        video_type = track.get("videoType")
        video_id = track.get("videoId")

        if video_type == "MUSIC_VIDEO_TYPE_ATV":
            atv_count += 1
        elif video_id:
            non_atv.append({
                "videoId": video_id,
                "title": track.get("title", "Unknown"),
                "artist": track.get("artists", [{}])[0].get("name", "Unknown") if track.get("artists") else "Unknown",
                "videoType": video_type,
            })

    print(f"\nArt Tracks (skip): {atv_count}")
    print(f"Non-ATV (export): {len(non_atv)}")

    if not non_atv:
        print("\nNo non-ATV tracks to export")
        return

    # Show sample
    print(f"\nSample tracks to export:")
    for t in non_atv[:5]:
        vtype = t["videoType"] or "UGC"
        print(f"  [{vtype}] {t['artist']} - {t['title']}")
    if len(non_atv) > 5:
        print(f"  ... and {len(non_atv) - 5} more")

    if args.dry_run:
        print(f"\n[DRY RUN] Would add {len(non_atv)} tracks to fallback playlist")
        return

    # Fetch target playlist to check for existing tracks
    print(f"\nFetching target playlist {args.target}...")
    target = yt.get_playlist(args.target, limit=None)
    existing = {t.get("videoId") for t in target.get("tracks", [])}
    print(f"Target has {len(existing)} existing tracks")

    # Filter out already-present tracks
    to_add = [t for t in non_atv if t["videoId"] not in existing]
    already = len(non_atv) - len(to_add)

    print(f"\nTo add: {len(to_add)}")
    print(f"Already in target: {already}")

    if to_add:
        print(f"\nSample tracks to add:")
        for t in to_add[:5]:
            print(f"  {t['videoId']} - {t['artist']} - {t['title']}")
        if len(to_add) > 5:
            print(f"  ... and {len(to_add) - 5} more")

    if not to_add:
        print("\nNothing new to add")
        return

    # Add to playlist
    print(f"\nAdding to fallback playlist...")
    video_ids = [t["videoId"] for t in to_add]
    batch_size = 50
    success = 0
    failed = 0

    for i in range(0, len(video_ids), batch_size):
        batch = video_ids[i:i + batch_size]
        try:
            yt.add_playlist_items(args.target, batch, duplicates=True)
            success += len(batch)
            print(f"  Batch {i // batch_size + 1}: {len(batch)} added")
        except Exception as e:
            print(f"  Error: {e}")
            failed += len(batch)

    print(f"\nDone! Added {success} to fallback playlist ({failed} failed)")


if __name__ == "__main__":
    main()
