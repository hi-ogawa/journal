#!/usr/bin/env python3
"""Import videos from jsonl/tsv to a YouTube Music playlist."""

import argparse
import csv
import json
import sys
from pathlib import Path

from ytmusicapi import YTMusic

AUTH_FILE = "data/ytmusicapi-browser.json"


def check_auth(yt: YTMusic) -> bool:
    """Verify credentials are valid with a lightweight API call."""
    try:
        yt.get_library_songs(limit=1)
        return True
    except Exception:
        return False


def load_video_ids_jsonl(path: Path, confidence: str | None = None) -> list[str]:
    """Load video IDs from results.jsonl, optionally filtering by exact confidence."""
    video_ids = []
    with open(path) as f:
        for line in f:
            record = json.loads(line)
            if record.get("error"):
                continue
            if confidence and record.get("confidence") != confidence:
                continue
            video_ids.append(record["video_id"])
    return video_ids


def load_video_ids_tsv(path: Path) -> list[str]:
    """Load video IDs from review TSV (extracts from URL column)."""
    video_ids = []
    with open(path) as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) >= 2:
                url = row[1]
                # Extract video ID from URL like https://youtube.com/watch?v=VIDEO_ID
                if "v=" in url:
                    video_id = url.split("v=")[1].split("&")[0]
                    video_ids.append(video_id)
    return video_ids


def get_existing_video_ids(yt: YTMusic, playlist_id: str) -> set[str]:
    """Fetch existing video IDs in playlist to avoid duplicates."""
    print(f"Fetching existing playlist contents...")
    playlist = yt.get_playlist(playlist_id, limit=None)
    existing = {track["videoId"] for track in playlist.get("tracks", []) if track.get("videoId")}
    print(f"  Found {len(existing)} existing tracks")
    return existing


def main():
    parser = argparse.ArgumentParser(description="Import videos to YouTube Music playlist")
    parser.add_argument("--input", "-i", required=True, help="Input file (jsonl or tsv)")
    parser.add_argument("--playlist", "-p", required=True, help="Target playlist ID")
    parser.add_argument("--confidence", "-c", choices=["high", "medium", "low", "none"],
                        help="Minimum confidence level (jsonl only)")
    parser.add_argument("--batch-size", "-b", type=int, default=50, help="Videos per batch (default: 50)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show what would be done")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)

    # Load video IDs based on file type
    if input_path.suffix == ".jsonl":
        video_ids = load_video_ids_jsonl(input_path, confidence=args.confidence)
    elif input_path.suffix == ".tsv":
        video_ids = load_video_ids_tsv(input_path)
    else:
        print(f"Error: Unsupported file type {input_path.suffix}")
        sys.exit(1)

    print(f"Loaded {len(video_ids)} video IDs from {input_path}")

    if args.dry_run:
        print(f"[DRY RUN] Would add {len(video_ids)} videos to playlist {args.playlist}")
        return

    # Initialize YTMusic
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

    # Get existing to avoid duplicates
    existing = get_existing_video_ids(yt, args.playlist)
    new_ids = [vid for vid in video_ids if vid not in existing]
    print(f"New videos to add: {len(new_ids)} (skipping {len(video_ids) - len(new_ids)} duplicates)")

    if not new_ids:
        print("Nothing to add")
        return

    # Add in batches
    for i in range(0, len(new_ids), args.batch_size):
        batch = new_ids[i:i + args.batch_size]
        print(f"Adding batch {i // args.batch_size + 1}: {len(batch)} videos...")
        try:
            result = yt.add_playlist_items(args.playlist, batch, duplicates=True)
            status = result.get("status", "unknown")
            print(f"  Result: {status}")
        except Exception as e:
            print(f"  Error: {e}")
            # Continue with next batch

    print("Done!")


if __name__ == "__main__":
    main()
