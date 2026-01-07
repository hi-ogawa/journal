# Anki Manual Knowledge Base

## Purpose

**Problem**: LLM hallucinations when asking Anki-specific questions lead to incorrect settings, non-existent features, and confusion about spaced repetition algorithms.

**Solution**: Build a ground-truth knowledge base from official Anki documentation for accurate LLM-assisted lookup.

## Goal

Create a **single markdown file** containing all Anki manual documentation to:
- Provide as custom instructions/context to LLM chat projects
- Enable accurate Anki Q&A without hallucinations
- Use with any LLM that supports large context windows

**Output**: `anki-manual-full.md`

## Approach

### Source

GitHub repo: https://github.com/ankitects/anki-manual
- mdBook format with markdown source in `src/`
- `SUMMARY.md` defines chapter order
- Already in markdown - no HTML conversion needed

### Steps

1. [x] Clone repo (without nested .git)
2. [x] Explore `SUMMARY.md` for chapter order
3. [x] Create concatenation script
4. [x] Generate `anki-manual-full.md`

### Output Stats

```
Lines:    7,680
Words:    50,584
Size:     335,249 bytes (0.32 MB)
Chapters: 56
```

### Commands

```bash
cd tasks/2026-01-07-anki-document

# Clone repo and remove nested .git
git clone --depth 1 https://github.com/ankitects/anki-manual.git data/anki-manual
rm -rf data/anki-manual/.git

# Explore structure
ls data/anki-manual/src/
cat data/anki-manual/src/SUMMARY.md

# Run concatenation
uv run scripts/concatenate.py
```

## Repository Structure

```
tasks/2026-01-07-anki-document/
├── plan.md                    # This file
├── pyproject.toml            # Python dependencies (minimal)
├── scripts/
│   └── concatenate.py        # Concatenate markdown files
├── data/
│   ├── anki-manual/          # ⚠️ GIT-IGNORED: Cloned repo
│   └── anki-manual-full.md   # 🎯 FINAL OUTPUT
└── .gitignore
```

## Notes

- Simpler than OBS task: source is already markdown
- Follow SUMMARY.md order for logical structure
- Include chapter headers for navigation
