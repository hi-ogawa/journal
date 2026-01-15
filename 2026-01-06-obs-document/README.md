# OBS Studio Knowledge Base

Scrape and convert OBS Studio's official knowledge base into a single markdown file for LLM context.

## Why

LLMs hallucinate OBS-specific settings and features. Providing official documentation as context enables accurate Q&A without external verification.

## Output

- `data/obs-kb-full.md` - 100 articles, 33K words, 0.2 MB

## Usage

```bash
# Scrape (wget)
wget --recursive --level=3 --random-wait -e robots=off \
     --adjust-extension --accept-regex='obsproject.com/kb/.*' \
     --directory-prefix=data/html https://obsproject.com/kb/

# Convert and concatenate
uv run scripts/convert-kb.py
uv run scripts/concatenate-kb.py
```
