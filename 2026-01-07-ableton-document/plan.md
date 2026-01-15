# Ableton Live 12 Documentation

## Purpose

**Problem**: LLM hallucinations when asking Ableton-specific questions lead to incorrect shortcuts, non-existent features, and wasted troubleshooting time.

**Solution**: Build a ground-truth knowledge base from official Ableton documentation, enabling accurate LLM-assisted lookup without external verification.

## Goal

Create a **single text file** (markdown) containing all Ableton Live 12 manual documentation to:
- Provide as custom instructions/context to LLM chat projects
- Enable accurate Ableton Q&A without hallucinations
- Use with any LLM that supports large context windows

**Output**: `ableton-manual-full.md` - single concatenated markdown file

## Approach

### Phase 1: Scraping
- Use wget to recursively download Ableton manual HTML
- Target: https://www.ableton.com/en/live-manual/12/

### Phase 2: Conversion
- Use BeautifulSoup to extract `#chapter_content` div
- Use html2text to convert to markdown (preserves tables)
- Parallel processing for performance

### Phase 3: Concatenation
- Combine all markdown files into single output
- Add metadata header

## Implementation Plan

### Step 1: Scrape with wget

```sh
cd tasks/2026-01-07-ableton-document

wget \
    --recursive \
    --level=2 \
    --random-wait \
    -e robots=off \
    --adjust-extension \
    --accept-regex='ableton.com/en/live-manual/12/.*' \
    --directory-prefix=data/html \
    https://www.ableton.com/en/live-manual/12/
```

**Notes**:
- `--level=2`: Manual index + chapter pages (42 chapters)
- `--accept-regex`: Only download manual pages, not whole site
- Output: `data/html/www.ableton.com/en/live-manual/12/`

### Step 2: Convert with html2text

```sh
uv run scripts/convert-manual.py
```

- Uses BeautifulSoup to extract `#chapter_content` div
- Uses html2text for markdown conversion (preserves tables)
- Parallel processing with 4 workers
- Note: trafilatura was tried first but dropped tables

### Step 3: Concatenate

```sh
uv run scripts/concatenate-manual.py
```

- Combines all markdown files into `data/ableton-manual-full.md`
- Adds header with metadata (date, chapter count, size)

## Repository Structure

```
tasks/2026-01-07-ableton-document/
├── plan.md                    # This file
├── pyproject.toml            # Python dependencies
├── workflow.md               # Personal workflow notes (verified)
├── scripts/
│   ├── convert-manual.py     # HTML → markdown conversion
│   └── concatenate-manual.py # Combine into single file
├── data/                     # GIT-IGNORED
│   ├── html/                 # Raw HTML from wget
│   ├── md/                   # Converted markdown files
│   └── ableton-manual-full.md # Final output
└── .gitignore
```

## Results

**Final Output**: `data/ableton-manual-full.md`

| Metric | Value |
|--------|-------|
| Chapters | 42 |
| Lines | 15,502 |
| Words | 228,357 |
| Size | 1,433,897 bytes (1.37 MB) |

**Comparison with previous approach** (aiohttp + bs4 + html2text):
- Previous: 228,954 words, 1.4 MB
- Current: 228,357 words, 1.37 MB
- Nearly identical output with simpler wget-based workflow

## Success Criteria

- [x] Generate single `ableton-manual-full.md` with all 42 chapters
- [x] File size ~1-2 MB (comparable to previous approach)
- [ ] Test: Ask 10 Ableton questions → get accurate answers
- [ ] LLM cites specific docs instead of hallucinating

## Reference

**Source URL**: https://www.ableton.com/en/live-manual/12/

**Chapters** (42 total):
1. Welcome to Live
2. First Steps
3. Live Concepts
4. Working with the Browser
5. Managing Files and Sets
6. Arrangement View
7. Session View
8. Clip View
9. Audio Clips, Tempo, and Warping
10. Editing MIDI
... (and 32 more)

## Copyright Notice

Do NOT commit `data/` contents to public repos. Official Ableton documentation is their intellectual property. Use scripts to regenerate locally.
