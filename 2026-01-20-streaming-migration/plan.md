# Plan

## Phase 1: Evaluate workflow viability ✅

**Question:** Can YouTube + YouTube Music replace VLC workflow?

**Research:** See `notes/youtube-music-library.md`
- Artists tab only shows Art Tracks (official music with ISRCs)
- Linked music videos can be added to library via YT Music
- Regular videos (covers, live performances) → Liked playlist only

**Conclusion:** Yes, workable.

New workflow:
1. Add to "Good music" playlist on YouTube
2. Async review on YT Music → "Add to library" if available
3. Listen on mobile

---

## Phase 2: Map local files → YouTube video IDs 🔄

### Data extraction

**Source:** 738 opus files in `D:\music\Download` (Windows)

**Filename format:** `Artist - Title.opus` (already searchable)

```bash
# Extract clean queries from Windows file list
grep '\.opus"$' data/files.txt | \
  sed 's|.*\\||; s|\.opus"$||; s|^"||' | \
  sort > data/queries.txt
```

### Search script

`scripts/search_youtube.py` - async batch YouTube search

**Usage:**
```bash
python search_youtube.py --start 0 --end 100      # test batch
python search_youtube.py --overwrite              # full run, overwrite
python search_youtube.py --concurrency 5          # slower, gentler
```

**How it works:**
- Runs `yt-dlp --flat-playlist -j "ytsearch1:{query}"` for each line
- Async with semaphore for parallel execution
- Outputs JSONL with: index, query, video_id, title, channel, view_count, confidence

**Confidence scoring:**
- `high` = artist in channel/title AND song in title
- `medium` = artist OR song matches
- `low` = neither matches (likely false positive)
- `none` = no search result

### Re-scoring

`scripts/rescore.py` - re-process confidence scores without re-searching

**Usage:**
```bash
uv run rescore.py                # re-score in place
uv run rescore.py -o new.jsonl   # output to different file
```

**Why separate script:**
- Tweak scoring algorithm without re-running 738 YouTube searches
- Normalizes punctuation (`-:_.'` etc.) for fuzzy matching
- Handles Windows filename artifacts (e.g., `ME-I` vs `ME:I`)

### Output

`data/results.jsonl` - one JSON object per line:
```json
{"index": 0, "query": "APRIL - Dream Candy", "video_id": "H2T1yZbTMzo", "title": "...", "channel": "1theK", "confidence": "high"}
```

### Manual review list

```bash
# Extract low/none confidence for manual review
jq -r 'select(.confidence == "low" or .confidence == "none") |
  "\(.index)\t\(.confidence)\t\(.query)\t\(.title // "N/A")\t\(.channel // "N/A")"' \
  data/results.jsonl | sort -n > data/review.tsv
```

`data/review.tsv` - tab-separated: index, youtube URL, confidence, query, matched title, matched channel

---

## Phase 3: Review & batch import (TODO)

1. Review low confidence matches manually
2. Add video IDs to "Good music" playlist (browser automation or API)
3. On YT Music: review playlist → "Add to library" for library-able songs

---

## Progress

### 2026-01-20

**Workflow research:**
- Researched YouTube Music library/Artists tab behavior
- Discovered Art Track vs linked video distinction
- Concluded: YT Music workflow can replace VLC

**Migration started:**
- Got file list from Windows (743 files, 738 opus)
- Created `scripts/search_youtube.py`
- Tested first 100: 99 matched, identified false positive issue on obscure artists
- Added confidence scoring to flag low-quality matches

**Full search completed:**
- Ran search on all 738 queries
- Created `scripts/rescore.py` for re-processing confidence scores
- Added punctuation normalization (fixes Windows filename artifacts like `ME-I` vs `ME:I`)
- Final stats: 545 high (74%), 158 medium (21%), 31 low (4%), 4 none (1%)
- 703/738 (95%) high or medium confidence → ready for import
- 35 items need manual review (`data/review.tsv`)

### 2026-01-21

**Manual review of low/none:**
- Reviewed 31 low + 4 none confidence items
- Dropped 19 low + 1 none (in `review-low-todo.tsv`, `review-none-todo.tsv`)
- Kept 12 low + 3 none → need manual search/correction
- See `notes/batch-import-options.md` for Phase 3 strategies
