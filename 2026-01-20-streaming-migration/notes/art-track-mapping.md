# Art Track ↔ Video Mapping Research

## The Problem

When you add an OMV (Official Music Video) to a YT Music playlist, the UI shows:
- Art Track thumbnail (not the video thumbnail you added)
- Song/Video toggle switch on the player page

Example:
- Art Track: https://music.youtube.com/watch?v=rT_isNWT4gQ (Dirty Loops - Next to You)
- Video: https://music.youtube.com/watch?v=rV9uCmlMQ1c (same song, music video version)

The toggle exists in the UI, meaning **YouTube Music knows the mapping**. But can we access it via API?

## What We Tried

### 1. Playlist API (`get_playlist`)

```python
playlist = yt.get_playlist(playlist_id, limit=None)
track = playlist['tracks'][0]  # The OMV
```

Response for OMV track:
```json
{
  "videoId": "rV9uCmlMQ1c",
  "title": "Next to You",
  "artists": [{"name": "Dirty Loops", "id": "..."}],
  "album": null,
  "videoType": "MUSIC_VIDEO_TYPE_OMV"
}
```

**Result:** No Art Track reference. `album` is `null`.

### 2. Song Details API (`get_song`)

```python
song = yt.get_song('rV9uCmlMQ1c')
```

Response keys: `playabilityStatus`, `streamingData`, `playbackTracking`, `videoDetails`, `microformat`

**Result:** No Art Track reference. Just playback metadata.

### 3. Watch Playlist API (`get_watch_playlist`)

The ytmusicapi docs mention a `counterpart` field for song/video toggle:

```python
watch = yt.get_watch_playlist('rV9uCmlMQ1c')
track = watch['tracks'][0]
print(track.get('counterpart'))  # None
```

Also tried from Art Track side:
```python
watch = yt.get_watch_playlist('rT_isNWT4gQ')  # Art Track
track = watch['tracks'][0]
print(track.get('counterpart'))  # None
```

**Result:** `counterpart` is `None` for both directions.

### 4. Tried Known Popular Songs

```python
results = yt.search('BTS Dynamite', filter='songs', limit=1)
watch = yt.get_watch_playlist(results[0]['videoId'])
print(watch['tracks'][0].get('counterpart'))  # None
```

**Result:** Still `None`. The `counterpart` field seems unreliable or deprecated.

## Why the Disconnect?

The YT Music web UI clearly has the Song/Video toggle, but ytmusicapi doesn't expose it. Possible reasons:

1. **Different API endpoint**: The web UI might use an internal endpoint not replicated in ytmusicapi
2. **Client-side mapping**: The toggle might be determined client-side using metadata we don't have access to
3. **ISRC-based matching**: YouTube likely uses ISRC codes to link Art Tracks and videos internally
4. **The `counterpart` parser exists but data isn't returned**: Looking at `ytmusicapi/parsers/watch.py`, the parser looks for `PPVWR` (playlistPanelVideoWrapperRenderer) which contains counterpart data, but this renderer might not be returned in all cases

## Relevant ytmusicapi Code

From `ytmusicapi/parsers/watch.py`:
```python
counterpart = None
if PPVWR in result:
    counterpart = result[PPVWR]["counterpart"][0]["counterpartRenderer"][PPVR]
    result = result[PPVWR]["primaryRenderer"]
# ...
if counterpart:
    track["counterpart"] = parse_watch_track(counterpart)
```

The parser exists, but the `PPVWR` renderer isn't present in the API response.

## Possible Solutions

### Option 1: Heuristic Search (Current Approach)

For each OMV/UGC track:
1. Search `{title} {artist}` with `filter='songs'`
2. Find matching ATV (Art Track) with same title + artist
3. Use the Art Track's album to get `feedbackTokens`
4. Add to library

**Pros:** Works, no reverse engineering needed
**Cons:** Slow (~1 search per track), may have false positives/negatives

### Option 2: Reverse Engineer the Web UI

1. Capture network requests when viewing a video with Song/Video toggle
2. Find the endpoint that returns counterpart data
3. Implement direct API call

**Investigation:**

`/youtubei/v1/player` response (`data/player-response.json`):
- Contains `videoDetails.musicVideoType` (e.g., `MUSIC_VIDEO_TYPE_ATV`)
- Contains streaming data, playability status
- **No counterpart/mapping data**

`/youtubei/v1/next` response (`data/next-response.json`):
- Captured from Art Track https://music.youtube.com/watch?v=rT_isNWT4gQ
- **Contains counterpart data!**

```
playlistPanelVideoWrapperRenderer
├── primaryRenderer (Art Track)
└── counterpart[]
    └── counterpartRenderer
        └── playlistPanelVideoRenderer
            ├── title: "Next to You"
            ├── videoId: "rV9uCmlMQ1c"  ← OMV
            └── musicVideoType: "MUSIC_VIDEO_TYPE_OMV"
```

Also includes `segmentMap` for timing alignment between versions.

**Why ytmusicapi returned None (earlier testing):**

Initial testing returned `counterpart: None`. Re-testing with fresh credentials:

```python
>>> watch = yt.get_watch_playlist("rT_isNWT4gQ")  # Art Track
>>> watch["tracks"][0].get("counterpart")
{'videoId': 'rV9uCmlMQ1c', 'title': 'Next to You', 'videoType': 'MUSIC_VIDEO_TYPE_OMV', ...}
```

**It works!** The issue was stale auth credentials. ytmusicapi's `get_watch_playlist` DOES return counterpart data when properly authenticated.

### Option 3: Use ISRC Metadata

If we could get the ISRC code for a video, we could look up the corresponding Art Track. But:
- ISRC isn't exposed in ytmusicapi responses
- Would require additional API calls

## Recommendation

**Option 2 is viable** - `get_watch_playlist` returns counterpart data with fresh auth.

For OMV → Art Track mapping:
```python
watch = yt.get_watch_playlist(omv_video_id)
counterpart = watch["tracks"][0].get("counterpart")
if counterpart and counterpart.get("videoType") == "MUSIC_VIDEO_TYPE_ATV":
    art_track_id = counterpart["videoId"]
```

For Art Track → OMV mapping (what we tested):
```python
watch = yt.get_watch_playlist(art_track_id)
counterpart = watch["tracks"][0].get("counterpart")
if counterpart and counterpart.get("videoType") == "MUSIC_VIDEO_TYPE_OMV":
    omv_id = counterpart["videoId"]
```

**Tested both directions (2026-01-21):**
- Art Track (rT_isNWT4gQ) → OMV (rV9uCmlMQ1c) ✓
- OMV (rV9uCmlMQ1c) → Art Track (rT_isNWT4gQ) ✓

**Note:** Not all tracks have counterparts. Use heuristic search (Option 1) as fallback.
