#!/usr/bin/env python3
"""
Concatenate Anki manual markdown files into a single file.
Follows the order defined in SUMMARY.md.

Usage:
    uv run scripts/concatenate.py
"""

import re
from pathlib import Path
from datetime import datetime


def parse_summary(summary_path: Path) -> list[tuple[str, str]]:
    """
    Parse SUMMARY.md to extract (title, filepath) pairs in order.
    """
    content = summary_path.read_text(encoding='utf-8')

    # Match markdown links: [Title](path.md)
    pattern = r'\[([^\]]+)\]\(([^)]+\.md)\)'
    matches = re.findall(pattern, content)

    return matches


def main():
    base_dir = Path(__file__).parent.parent
    src_dir = base_dir / 'data' / 'anki-manual' / 'src'
    summary_path = src_dir / 'SUMMARY.md'
    output_file = base_dir / 'data' / 'anki-manual-full.md'

    # Parse SUMMARY.md for chapter order
    chapters = parse_summary(summary_path)
    print(f"Found {len(chapters)} chapters in SUMMARY.md")
    print(f"Output: {output_file}")
    print()

    # Prepare header
    header = f"""# Anki Manual

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source**: https://docs.ankiweb.net/
**Chapters**: {len(chapters)}

---

"""

    # Concatenate all files
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open('w', encoding='utf-8') as out:
        out.write(header)

        for i, (title, filepath) in enumerate(chapters, 1):
            md_path = src_dir / filepath

            if not md_path.exists():
                print(f"[{i}/{len(chapters)}] SKIP {filepath} (not found)")
                continue

            content = md_path.read_text(encoding='utf-8').strip()

            if not content:
                print(f"[{i}/{len(chapters)}] SKIP {filepath} (empty)")
                continue

            # Write chapter delimiter and content
            out.write(f"\n<!-- Chapter: {title} -->\n")
            out.write(f"<!-- Source: {filepath} -->\n\n")
            out.write(content)
            out.write("\n\n---\n")

            print(f"[{i}/{len(chapters)}] OK {filepath}")

    # Final statistics
    output_size = output_file.stat().st_size
    output_text = output_file.read_text(encoding='utf-8')
    line_count = output_text.count('\n')
    word_count = len(output_text.split())

    print()
    print("=" * 60)
    print("Concatenation complete!")
    print()
    print(f"Output: {output_file}")
    print(f"  Lines:    {line_count:,}")
    print(f"  Words:    {word_count:,}")
    print(f"  Size:     {output_size:,} bytes ({output_size / 1024 / 1024:.2f} MB)")
    print(f"  Chapters: {len(chapters)}")


if __name__ == '__main__':
    main()
