#!/usr/bin/env python3
"""
Concatenate all Ableton manual markdown files into a single file.

Usage:
    uv run scripts/concatenate-manual.py
"""

from pathlib import Path
from datetime import datetime
import re


def extract_chapter_number_from_content(filepath: Path) -> int:
    """Extract chapter number from markdown content (e.g., '# 1. Welcome to Live')."""
    try:
        content = filepath.read_text(encoding='utf-8')
        # Look for pattern like "# 1. " or "# 42. " at start of a line
        match = re.search(r'^#\s+(\d+)\.', content, re.MULTILINE)
        if match:
            return int(match.group(1))
    except Exception:
        pass
    return 999  # Put unnumbered files at the end


def main():
    # Define paths
    base_dir = Path(__file__).parent.parent
    md_root = base_dir / 'data' / 'md'
    output_file = base_dir / 'data' / 'ableton-manual-full.md'

    if not md_root.exists():
        print(f"Error: Markdown directory not found: {md_root}")
        print("Run convert-manual.py first.")
        return 1

    # Find all markdown files in subdirectories (exclude root index.md)
    md_files = [
        f for f in md_root.rglob('*.md')
        if f.parent != md_root  # Exclude root-level files
    ]
    md_files = sorted(md_files, key=extract_chapter_number_from_content)

    if not md_files:
        print(f"Error: No markdown files found in {md_root}")
        return 1

    print(f"Found {len(md_files)} markdown files")
    print(f"Output: {output_file}")
    print()

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Concatenate all files
    with output_file.open('w', encoding='utf-8') as out:
        # Write header
        out.write("# Ableton Live 12 Manual\n\n")
        out.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"**Source**: https://www.ableton.com/en/live-manual/12/\n")
        out.write(f"**Chapters**: {len(md_files)}\n\n")
        out.write("---\n\n")

        # Write each chapter
        for i, md_file in enumerate(md_files, 1):
            slug = md_file.parent.name  # Use directory name as slug
            print(f"[{i}/{len(md_files)}] {slug}")

            content = md_file.read_text(encoding='utf-8')

            # Write chapter header and content
            out.write(f"## Chapter: {slug}\n\n")
            out.write(content.strip())
            out.write("\n\n---\n\n")

    # Show statistics
    stats = output_file.stat()
    line_count = sum(1 for _ in output_file.open('r', encoding='utf-8'))
    word_count = sum(len(line.split()) for line in output_file.open('r', encoding='utf-8'))

    print()
    print("=" * 60)
    print(f"Concatenation complete!")
    print()
    print(f"Output: {output_file}")
    print(f"  Lines:  {line_count:,}")
    print(f"  Words:  {word_count:,}")
    print(f"  Size:   {stats.st_size:,} bytes ({stats.st_size / 1024 / 1024:.2f} MB)")

    return 0


if __name__ == '__main__':
    exit(main())
