#!/usr/bin/env python3
"""
Concatenate all markdown files into a single obs-kb-full.md file.

Usage:
    uv run scripts/concatenate-kb.py
"""

from pathlib import Path
from datetime import datetime


def main():
    # Define paths
    base_dir = Path(__file__).parent.parent
    md_root = base_dir / 'data' / 'md' / 'obsproject.com' / 'kb'
    output_file = base_dir / 'data' / 'obs-kb-full.md'

    # Find all markdown files (exclude category pages)
    md_files = sorted([
        f for f in md_root.rglob('*.md')
        if 'category' not in f.parts
    ])

    print(f"Found {len(md_files)} markdown files")
    print(f"Input:  {md_root}")
    print(f"Output: {output_file}")
    print()

    # Prepare header
    total_size = sum(f.stat().st_size for f in md_files)
    header = f"""# OBS Studio Knowledge Base

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source**: https://obsproject.com/kb
**Articles**: {len(md_files)}
**Size**: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)

---

"""

    # Concatenate all files
    with output_file.open('w', encoding='utf-8') as out:
        # Write header
        out.write(header)

        # Process each file
        for i, md_file in enumerate(md_files, 1):
            # Get article title from filename (slug)
            slug = md_file.stem
            title = slug.replace('-', ' ').title()

            # Read content
            content = md_file.read_text(encoding='utf-8').strip()

            # Skip empty files
            if not content:
                print(f"[{i}/{len(md_files)}] SKIP {slug} (empty)")
                continue

            # Write article delimiter and content
            out.write(f"\n## Article: {title}\n")
            out.write(f"**Slug**: `{slug}`\n\n")
            out.write(content)
            out.write("\n\n---\n")

            print(f"[{i}/{len(md_files)}] OK {slug}")

    # Final statistics
    output_size = output_file.stat().st_size
    line_count = output_file.read_text(encoding='utf-8').count('\n')
    word_count = len(output_file.read_text(encoding='utf-8').split())

    print()
    print("=" * 60)
    print(f"Concatenation complete!")
    print()
    print(f"Output: {output_file}")
    print(f"  Lines: {line_count:,}")
    print(f"  Words: {word_count:,}")
    print(f"  Size:  {output_size:,} bytes ({output_size / 1024 / 1024:.2f} MB)")


if __name__ == '__main__':
    main()
