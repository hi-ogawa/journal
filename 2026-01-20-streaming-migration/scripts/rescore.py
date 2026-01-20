#!/usr/bin/env python3
"""Re-score existing search results without re-running YouTube searches."""

import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
RESULTS_FILE = DATA_DIR / "results.jsonl"


def normalize(s: str) -> str:
    """Normalize string for fuzzy matching: lowercase, strip punctuation."""
    s = s.lower()
    s = re.sub(r"[-:_.'\"()[\]!?]", "", s)  # strip common punctuation
    s = re.sub(r"\s+", " ", s).strip()  # collapse whitespace
    return s


def compute_confidence(query: str, title: str | None, channel: str | None) -> str:
    """Compute match confidence with punctuation normalization."""
    if not title and not channel:
        return "none"

    query_norm = normalize(query)
    title_norm = normalize(title or "")
    channel_norm = normalize(channel or "")

    # Split query into artist and song title
    parts = query.split(" - ", 1)
    artist = normalize(parts[0]) if parts else ""
    song = normalize(parts[1]) if len(parts) > 1 else ""

    artist_match = artist and (artist in channel_norm or artist in title_norm)
    song_match = song and song in title_norm

    if artist_match and song_match:
        return "high"
    elif artist_match or song_match:
        return "medium"
    else:
        return "low"


def main(output: str | None = None, show_changes: bool = False):
    """Re-score all results."""
    if not RESULTS_FILE.exists():
        print(f"Error: {RESULTS_FILE} not found")
        return

    results = []
    changes = []

    with RESULTS_FILE.open() as f:
        for line in f:
            r = json.loads(line)
            old_conf = r["confidence"]
            new_conf = compute_confidence(r["query"], r["title"], r["channel"])

            if old_conf != new_conf:
                changes.append((r["index"], r["query"], old_conf, new_conf))

            r["confidence"] = new_conf
            results.append(r)

    # Sort by index for consistent output
    results.sort(key=lambda r: r["index"])

    # Write output
    out_path = Path(output) if output else RESULTS_FILE
    with out_path.open("w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Summary
    by_conf = {"high": 0, "medium": 0, "low": 0, "none": 0}
    for r in results:
        by_conf[r["confidence"]] += 1

    print(f"Re-scored {len(results)} results → {out_path}")
    print(f"  High:   {by_conf['high']}")
    print(f"  Medium: {by_conf['medium']}")
    print(f"  Low:    {by_conf['low']}")
    print(f"  None:   {by_conf['none']}")

    if changes:
        print(f"\n{len(changes)} confidence changes:")
        for idx, query, old, new in changes:
            arrow = "↑" if ["none", "low", "medium", "high"].index(new) > ["none", "low", "medium", "high"].index(old) else "↓"
            print(f"  [{idx}] {old} → {new} {arrow} {query[:50]}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Re-score search results with updated algorithm")
    parser.add_argument("-o", "--output", help="Output file (default: overwrite results.jsonl)")
    parser.add_argument("--show-changes", action="store_true", help="Show what changed")
    args = parser.parse_args()

    main(args.output, args.show_changes)
