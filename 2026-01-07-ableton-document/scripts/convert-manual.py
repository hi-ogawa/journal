#!/usr/bin/env python3
"""
Convert Ableton manual HTML files to markdown using html2text + BeautifulSoup.

Usage:
    uv run scripts/convert-manual.py
"""

from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import html2text
from bs4 import BeautifulSoup


def convert_file(html_path: Path, html_root: Path, md_root: Path) -> tuple[Path, bool, str]:
    """
    Convert a single HTML file to markdown.

    Returns:
        (output_path, success, error_message)
    """
    try:
        # Calculate relative path and output path
        rel_path = html_path.relative_to(html_root)
        md_path = md_root / rel_path.with_suffix('.md')

        # Create output directory
        md_path.parent.mkdir(parents=True, exist_ok=True)

        # Read HTML
        html_content = html_path.read_text(encoding='utf-8')

        # Extract chapter content div
        soup = BeautifulSoup(html_content, 'html.parser')
        chapter_div = soup.find('div', id='chapter_content')

        if not chapter_div:
            return (md_path, False, "No #chapter_content div found")

        # Convert to markdown
        h = html2text.HTML2Text()
        h.body_width = 0  # Don't wrap lines
        h.ignore_links = False
        h.ignore_images = False
        markdown = h.handle(str(chapter_div))

        if markdown.strip():
            md_path.write_text(markdown, encoding='utf-8')
            return (md_path, True, "")
        else:
            return (md_path, False, "No content extracted")

    except Exception as e:
        return (md_path, False, str(e))


def main():
    # Define paths
    base_dir = Path(__file__).parent.parent
    html_root = base_dir / 'data' / 'html' / 'www.ableton.com' / 'en' / 'live-manual' / '12'
    md_root = base_dir / 'data' / 'md'

    if not html_root.exists():
        print(f"Error: HTML directory not found: {html_root}")
        print()
        print("Run wget first:")
        print("  wget --recursive --level=2 --random-wait -e robots=off \\")
        print("       --adjust-extension --accept-regex='ableton.com/en/live-manual/12/.*' \\")
        print("       --directory-prefix=data/html https://www.ableton.com/en/live-manual/12/")
        return 1

    # Find all HTML files
    html_files = list(html_root.rglob('*.html'))

    total = len(html_files)
    print(f"Found {total} HTML files to convert")
    print(f"Input:  {html_root}")
    print(f"Output: {md_root}")
    print()

    if total == 0:
        print("No HTML files found!")
        return 1

    # Convert files in parallel
    success_count = 0
    error_count = 0
    errors = []

    with ProcessPoolExecutor(max_workers=4) as executor:
        # Submit all tasks
        futures = {
            executor.submit(convert_file, html_file, html_root, md_root): html_file
            for html_file in html_files
        }

        # Process results as they complete
        for i, future in enumerate(as_completed(futures), 1):
            html_file = futures[future]
            md_path, success, error_msg = future.result()

            if success:
                success_count += 1
                status = "OK"
            else:
                error_count += 1
                status = "ERR"
                errors.append((html_file.name, error_msg))

            # Show progress
            print(f"[{i}/{total}] {status} {html_file.name}")

    # Summary
    print()
    print("=" * 60)
    print(f"Conversion complete!")
    print(f"  Success: {success_count}")
    print(f"  Errors:  {error_count}")

    if errors:
        print()
        print("Errors encountered:")
        for filename, msg in errors:
            print(f"  - {filename}: {msg}")

    # Show output statistics
    md_files = list(md_root.rglob('*.md'))
    total_size = sum(f.stat().st_size for f in md_files)
    print()
    print(f"Output statistics:")
    print(f"  Files: {len(md_files)}")
    print(f"  Size:  {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)")

    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    exit(main())
