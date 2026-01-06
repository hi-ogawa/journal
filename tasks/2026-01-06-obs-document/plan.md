# OBS Studio Knowledge Base

## Purpose

**Problem**: LLM hallucinations when asking OBS-specific questions lead to incorrect settings, non-existent features, and wasted troubleshooting time.

**Solution**: Build a ground-truth knowledge base from official OBS documentation, enabling accurate LLM-assisted lookup without external verification.

## Goal

Create a **single text file** (markdown) containing all OBS knowledge base documentation to:
- Provide as custom instructions/context to Gemini chat projects
- Enable accurate OBS Q&A without hallucinations
- Use with any LLM that supports large context windows

**Output**: `obs-kb-full.md` - single concatenated markdown file, similar to Ableton reference

## Approach

### Phase 1: Estimation
- Explore OBS KB structure (https://obsproject.com/kb)
- Count total pages/articles
- Identify article categories and organization
- Estimate total content size

### Phase 2: Scraping and Conversion
- Scrape official OBS knowledge base
- Convert HTML to markdown format
- Preserve structure and metadata

### Phase 3: Validation
- Test LLM retrieval accuracy with real questions
- Verify: Can LLM answer accurately without hallucinating?
- Document coverage and limitations

## Repository Structure

```
tasks/2026-01-06-obs-document/
├── plan.md                    # This file
├── pyproject.toml            # Python dependencies
├── scripts/
│   ├── estimate-kb.py        # Count articles and estimate size
│   ├── fetch-kb.py           # Scrape OBS knowledge base
│   └── convert-kb.py         # Convert to single markdown file
├── data/
│   ├── html/                 # ⚠️ GIT-IGNORED: Raw HTML articles
│   └── obs-kb-full.md        # 🎯 FINAL OUTPUT: Single markdown file
└── README.md                 # Documentation and usage
```

## Success Criteria

- ✅ Generate single `obs-kb-full.md` file with all KB articles
- ✅ File size comparable to Ableton reference (~1-2 MB)
- ✅ Compatible with Gemini's context window (2M tokens)
- ✅ Test: Ask 10 OBS questions → get accurate answers
- ✅ LLM cites specific docs instead of hallucinating
- ✅ No need to verify answers against external sources

## Implementation Plan

### Step 1: Exploration
- [x] Manual exploration of KB structure (see `estimation.md`)
- [x] Identified 10 categories, URL patterns, pagination structure

### Step 2: Scraping

- [x] wget iterate then one-shot

```sh
wget \
     --recursive \
     --level=3 \
     --random-wait \
     -e robots=off \
     --adjust-extension \
     --accept-regex='obsproject.com/kb/.*' \
     --directory-prefix=data/html \
     https://obsproject.com/kb/
```

### Step 3: Conversion Script

- [x] convert each html into markdown
  - Created `scripts/convert-kb.py` - Python wrapper using trafilatura library
  - Parallel processing with 4 workers for performance
  - Successfully converted 100 HTML files to markdown (0.20 MB)
  - Excluded category/pagination pages from conversion

```sh
uv run scripts/convert-kb.py
```

- [x] Concatenate into single `obs-kb-full.md` file
  - Created `scripts/concatenate-kb.py`
  - Added header with metadata (date, article count, size)
  - Preserved article structure with clear delimiters
  - Each article includes title and slug for reference

```sh
uv run scripts/concatenate-kb.py
```

- [x] Output stats (lines, words, size)
  - **Lines**: 4,498
  - **Words**: 33,223
  - **Size**: 212,448 bytes (0.20 MB)
  - **Articles**: 100

### Step 4: Testing
- [ ] Test with real OBS questions
- [ ] Verify accuracy vs. hallucinations
- [ ] Document limitations

## Initial Exploration Findings

**See**: `estimation.md` for detailed analysis

### Quick Summary
- **Categories**: 10 (F.A.Q.s, Getting Started, Troubleshooting, OBS Studio, Streaming, Recording, Sources & Filters, Audio, Scripting, Post-Production)
- **Estimated articles**: 100-150 total
- **Estimated size**: 40,000-90,000 words (~0.3-0.6 MB)
- **Comparison**: Smaller than Ableton docs (228,954 words, 1.4 MB)
- **Structure**: Clean URL patterns, paginated categories
- **Sample article**: ~450-500 words with screenshots

### URL Patterns
```
Categories:  https://obsproject.com/kb/category/{0-9}?page={N}
Articles:    https://obsproject.com/kb/{article-slug}
```

## Reference

Inspired by: `C:\Users\hiroshi\code\personal\misc\llm\ableton\README.md`
- Similar methodology: scrape official docs → markdown → LLM context
- Proven approach for avoiding hallucinations

### Ableton Docs Stats (Reference)

File: `C:\Users\hiroshi\code\personal\misc\llm\ableton\data\custom-instructions\ableton-docs-full.md`

```
Lines:      15,848
Words:     228,954
Size:    1,441,333 bytes (~1.4 MB)
Chapters:       42
```

**Expectation**: OBS KB documentation may be similar or smaller in scope.
- Estimate during Phase 1 to compare
- Use as baseline for LLM context size
