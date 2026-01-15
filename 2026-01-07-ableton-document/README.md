# Ableton Live 12 Documentation

Scrape and convert Ableton Live 12's official manual into a single markdown file for LLM context.

## Why

LLMs hallucinate Ableton shortcuts and features. Providing official documentation as context enables accurate Q&A without external verification.

## Output

- `data/ableton-manual-full.md` - 42 chapters, 228K words, 1.4 MB

## Usage

```bash
# Scrape (wget)
wget --recursive --level=2 --random-wait -e robots=off \
     --adjust-extension --accept-regex='ableton.com/en/live-manual/12/.*' \
     --directory-prefix=data/html https://www.ableton.com/en/live-manual/12/

# Convert and concatenate
uv run scripts/convert-manual.py
uv run scripts/concatenate-manual.py
```

## Note

Do NOT commit `data/` to public repos - Ableton documentation is their intellectual property.
