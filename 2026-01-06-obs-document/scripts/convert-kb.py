#!/usr/bin/env python3
"""
Convert HTML files to markdown using trafilatura.

Usage:
    uv run scripts/convert-kb.py
"""

from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import trafilatura

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

        # Read HTML and convert to markdown
        html_content = html_path.read_text(encoding='utf-8')
        markdown = trafilatura.extract(
            html_content,
            output_format='markdown',
            include_comments=False,
            include_tables=True,
            include_images=True,
            include_links=True,
        )

        if markdown:
            md_path.write_text(markdown, encoding='utf-8')
            return (md_path, True, "")
        else:
            return (md_path, False, "No content extracted")

    except Exception as e:
        return (md_path, False, str(e))


def main():
    # Define paths
    base_dir = Path(__file__).parent.parent
    html_root = base_dir / 'data' / 'html' / 'obsproject.com' / 'kb'
    md_root = base_dir / 'data' / 'md' / 'obsproject.com' / 'kb'

    # Find all HTML files (exclude category pages and pagination)
    html_files = [
        f for f in html_root.rglob('*.html')
        if 'category' not in f.parts  # Skip category index pages
    ]

    total = len(html_files)
    print(f"Found {total} HTML files to convert")
    print(f"Input:  {html_root}")
    print(f"Output: {md_root}")
    print()

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


if __name__ == '__main__':
    main()
