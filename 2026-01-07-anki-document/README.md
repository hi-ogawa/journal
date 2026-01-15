# Anki Manual Knowledge Base

Concatenate the official Anki manual (already markdown) into a single file for LLM context.

## Why

LLMs hallucinate Anki settings and spaced repetition algorithm details. Providing official documentation as context enables accurate Q&A.

## Output

- `data/anki-manual-full.md` - 56 chapters, 50K words, 0.3 MB

## Usage

```bash
# Clone repo (source is already markdown)
git clone --depth 1 https://github.com/ankitects/anki-manual.git data/anki-manual
rm -rf data/anki-manual/.git

# Concatenate
uv run scripts/concatenate.py
```
