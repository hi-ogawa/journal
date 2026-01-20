#!/usr/bin/env python3
"""Add eligible songs from a playlist to YT Music library (Artists tab).

Only adds direct Art Tracks (ATVs) that have feedbackTokens.
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
    parser = argparse.ArgumentParser(description="Add playlist songs to YT Music library")
    parser.add_argument("--playlist", "-p", required=True, help="Source playlist ID")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show what would be done")
    args = parser.parse_args()

    yt = YTMusic(AUTH_FILE)

    # Verify auth is valid
    print("Checking credentials...")
    if not check_auth(yt):
        print("Error: Auth credentials are stale. Please refresh:")
        print("  1. Go to music.youtube.com (logged in)")
        print("  2. DevTools → Network → find any POST request")
        print("  3. Run: uv run ytmusicapi browser")
        sys.exit(1)
    print("Auth OK")

    # Fetch playlist
    print(f"Fetching playlist {args.playlist}...")
    playlist = yt.get_playlist(args.playlist, limit=None)

    tracks = playlist.get("tracks", [])
    print(f"Found {len(tracks)} tracks")

    # Collect tokens directly from playlist
    add_tokens = []
    already_in_library = 0
    no_token = 0
    skipped = 0

    for track in tracks:
        video_type = track.get("videoType")
        tokens = track.get("feedbackTokens")

        if video_type != "MUSIC_VIDEO_TYPE_ATV":
            skipped += 1
            continue

        if track.get("inLibrary"):
            already_in_library += 1
            continue

        if tokens and tokens.get("add"):
            add_tokens.append(tokens["add"])
        else:
            no_token += 1

    print(f"\nArt Tracks to add: {len(add_tokens)}")
    print(f"Already in library: {already_in_library}")
    print(f"Skipped (OMV/UGC): {skipped}")
    if no_token:
        print(f"No token: {no_token}")

    if not add_tokens:
        print("\nNothing to add")
        return

    if args.dry_run:
        print(f"\n[DRY RUN] Would add {len(add_tokens)} tracks to library")
        return

    # Add to library
    print(f"\nAdding to library...")
    batch_size = 50
    success = 0
    failed = 0

    for i in range(0, len(add_tokens), batch_size):
        batch = add_tokens[i:i + batch_size]
        try:
            yt.edit_song_library_status(batch)
            success += len(batch)
            print(f"  Batch {i // batch_size + 1}: {len(batch)} added")
        except Exception as e:
            print(f"  Error: {e}")
            failed += len(batch)

    print(f"\nDone! Added {success} to library ({failed} failed)")


if __name__ == "__main__":
    main()
