# Plan

## Phase 1: Map local files → YouTube video IDs

### Finding: No video ID stored

Checked `yt-dlp-gui` source (`server.ts:72-82`):
- Metadata written: `title`, `artist`, `album`, thumbnail
- Video ID NOT stored in file or filename
- No database/history tracking

**Must use search-based matching.**

### Approach: Search-based matching

**Input:** Local opus files with metadata (artist, title, album, thumbnail)

**Output:** Mapping file (JSON/CSV)
```
{
  "files": [
    {
      "path": "/path/to/file.opus",
      "artist": "Artist Name",
      "title": "Song Title",
      "video_id": "dQw4w9WgXcQ",
      "confidence": "high",  // high | medium | manual
      "match_source": "youtube_search"
    }
  ]
}
```

### Search methods (in order of preference)

**1. yt-dlp ytsearch (no quota, free)**
```bash
yt-dlp --flat-playlist -j "ytsearch5:{artist} {title}"
```
- Returns top N results with video IDs, channel names, view counts
- No API quota limits
- Can filter by channel name match

**2. YouTube Data API v3**
- Official API, more structured response
- 10,000 quota units/day (search = 100 units = 100 searches/day)
- Better for small collections

**3. Thumbnail reverse search (experimental)**
- Each file has embedded thumbnail from `i.ytimg.com/vi/{id}/hqdefault.jpg`
- If we could extract and reverse-search... but YouTube doesn't support this directly
- Could hash thumbnails and compare against fetched thumbnails from search results

### Matching strategy

```
For each file:
  1. Extract (artist, title) from opus metadata
  2. Search YouTube: "{artist} {title}"
  3. Score each result:
     - Channel name matches artist? +10
     - Title contains our title? +5
     - View count > 100k? +2
  4. If top score >> second score: auto-accept (high confidence)
     Else: flag for manual review (medium confidence)
```

### Edge cases
- Time-range clips → skip, keep local only (no single video maps)
- Deleted/private videos → won't match, accept loss or find re-upload
- Cover vs original → channel name matching helps
- Same song, multiple uploads → prefer official channel, higher views

---

## Phase 2: Batch import to streaming platform

Once we have video IDs from Phase 1, we can target any platform.

### Method comparison

| Method | Pros | Cons |
|--------|------|------|
| Browser automation | Simple auth (just login), visual feedback, works on any platform | Slower, fragile to UI changes |
| Unofficial API (`ytmusicapi`) | Fast, reliable | Auth setup, may break |
| Official API (Spotify) | Stable, documented | OAuth flow, not all content exists |

### Browser automation (Playwright/Puppeteer)

```
For each video_id:
  1. Navigate to youtube.com/watch?v={video_id}
  2. Wait for page load
  3. Click "Like" button (or "Save to playlist" → select playlist)
  4. Small delay to avoid rate limiting
```

Benefits:
- Auth: just log in manually once, session persists
- Visible: can watch it work, catch errors
- Portable: same approach works for YouTube, Spotify web, etc.

Could also do:
- Open `music.youtube.com/watch?v={video_id}` → click "Add to library"
- Batch add to a YouTube playlist first, then manually "Save all to library"

### Platform-specific APIs

**YouTube Music** - `ytmusicapi`
- `rate_song(video_id, 'LIKE')` → adds to library + Artists tab
- OAuth via browser cookies

**Spotify** - Official Web API
- Search artist+title → Spotify track ID
- `PUT /me/tracks` → add to library
- Caveat: covers, live performances may not exist

**Other platforms**
- Apple Music: MusicKit API
- Tidal: API available

### Recommendation

Start with browser automation for simplicity. If too slow or flaky, switch to API.

---

## Summary: Data flow

```
Local opus files (artist, title metadata)
        │
        ▼
   Phase 1: Search matching
        │
        ▼
   Mapping file (file → video_id)
        │
        ├──► YouTube Music (ytmusicapi)
        │
        ├──► Spotify (search artist+title → Spotify ID → add)
        │
        └──► Future platforms
```

The mapping file becomes your canonical "collection" - portable across platforms.

---

## Questions to resolve

- [ ] How many songs in VLC collection? (determines if manual review is feasible)
- [ ] Where are the opus files located? (path to scan)
- [ ] Edge cases: time-range clips, multi-song videos → skip or handle separately?

---

## Next steps

1. **Inventory**: Count files, check metadata quality
2. **Prototype**: Script to extract metadata + search YouTube for a few files
3. **Batch run**: Generate full mapping file with confidence scores
4. **Review**: Manual check on medium/low confidence matches
5. **Import**: Pick platform, run batch import

---

## Progress

### 2026-01-20
- Created task directory
- Reviewed yt-dlp-gui source - confirmed no video ID stored in files
- Brainstormed Phase 1 (search-based matching) and Phase 2 (platform import)
- Decided: mapping file as portable canonical collection
