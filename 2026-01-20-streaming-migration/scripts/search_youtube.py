#!/usr/bin/env python3
"""Search YouTube for video IDs matching local file queries."""

import asyncio
import json
import sys
from pathlib import Path

QUERIES_FILE = Path(__file__).parent.parent / "data" / "queries.txt"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "results.jsonl"


def compute_confidence(query: str, title: str | None, channel: str | None) -> str:
    """Compute match confidence based on query vs title/channel similarity."""
    if not title and not channel:
        return "none"

    query_lower = query.lower()
    title_lower = (title or "").lower()
    channel_lower = (channel or "").lower()

    # Split query into artist and song title
    parts = query.split(" - ", 1)
    artist = parts[0].lower() if parts else ""
    song = parts[1].lower() if len(parts) > 1 else ""

    artist_match = artist and (artist in channel_lower or artist in title_lower)
    song_match = song and song in title_lower

    if artist_match and song_match:
        return "high"
    elif artist_match or song_match:
        return "medium"
    else:
        return "low"


async def search_youtube(index: int, query: str) -> dict:
    """Search YouTube for a single query using yt-dlp."""
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "--flat-playlist",
        "-j",
        f"ytsearch1:{query}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    result = {"index": index, "query": query, "video_id": None, "title": None, "channel": None, "view_count": None, "confidence": "none", "error": None}

    if proc.returncode != 0:
        result["error"] = stderr.decode().strip()
        return result

    try:
        data = json.loads(stdout.decode())
        result["video_id"] = data.get("id")
        result["title"] = data.get("title")
        result["channel"] = data.get("channel")
        result["view_count"] = data.get("view_count")
        result["confidence"] = compute_confidence(query, result["title"], result["channel"])
    except json.JSONDecodeError as e:
        result["error"] = f"JSON decode error: {e}"

    return result


async def main(start: int = 0, end: int | None = None, concurrency: int = 10, overwrite: bool = False):
    """Run batch YouTube searches."""
    all_queries = QUERIES_FILE.read_text().strip().split("\n")
    queries = [(i + start, q) for i, q in enumerate(all_queries[start:end])]

    print(f"Searching {len(queries)} queries (index {start} to {start + len(queries) - 1})...")
    print(f"Concurrency: {concurrency}")

    # Load existing results to skip (for resume)
    existing_indices = set()
    if not overwrite and OUTPUT_FILE.exists():
        with OUTPUT_FILE.open() as f:
            for line in f:
                try:
                    existing_indices.add(json.loads(line)["index"])
                except:
                    pass
        if existing_indices:
            print(f"Resuming: {len(existing_indices)} already done, skipping...")

    queries = [(idx, q) for idx, q in queries if idx not in existing_indices]
    if not queries:
        print("All queries already processed.")
        return

    print(f"Processing {len(queries)} queries...")

    semaphore = asyncio.Semaphore(concurrency)
    completed = 0
    results = []

    # Open file for streaming writes
    mode = "w" if overwrite else "a"
    outfile = OUTPUT_FILE.open(mode)

    async def limited_search(idx: int, q: str):
        nonlocal completed
        async with semaphore:
            result = await search_youtube(idx, q)
            completed += 1
            conf = result["confidence"][0].upper() if result["video_id"] else "✗"
            print(f"[{completed}/{len(queries)}] {conf} [{idx}] {q[:50]}")
            # Stream write immediately
            outfile.write(json.dumps(result, ensure_ascii=False) + "\n")
            outfile.flush()
            return result

    # Gather preserves order in results
    results = await asyncio.gather(*[limited_search(idx, q) for idx, q in queries])
    outfile.close()

    # Summary
    by_conf = {"high": [], "medium": [], "low": [], "none": []}
    for r in results:
        by_conf[r["confidence"]].append(r)

    print(f"\nDone: {len(results)} total")
    print(f"  High:   {len(by_conf['high'])}")
    print(f"  Medium: {len(by_conf['medium'])}")
    print(f"  Low:    {len(by_conf['low'])}")
    print(f"  None:   {len(by_conf['none'])}")

    if by_conf["low"]:
        print(f"\n⚠️  Low confidence ({len(by_conf['low'])}):")
        for r in by_conf["low"][:10]:  # Show first 10
            print(f"  [{r['index']}] {r['query'][:40]}")
            print(f"       → {r['title'][:50] if r['title'] else 'N/A'}")
        if len(by_conf["low"]) > 10:
            print(f"  ... and {len(by_conf['low']) - 10} more")

    if by_conf["none"]:
        print(f"\n❌ No match ({len(by_conf['none'])}):")
        for r in by_conf["none"]:
            print(f"  [{r['index']}] {r['query']}")

    print(f"\nResults written to {OUTPUT_FILE}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0, help="Start index")
    parser.add_argument("--end", type=int, default=None, help="End index")
    parser.add_argument("--concurrency", type=int, default=10, help="Parallel requests")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite output file (default: append)")
    args = parser.parse_args()

    asyncio.run(main(args.start, args.end, args.concurrency, args.overwrite))
