# Batch Import Options

Two approaches that avoid YouTube Data API setup.

---

## Option 2: Browser Automation (Playwright)

### How it works

1. Launch browser with saved YouTube session (cookies)
2. For each video ID:
   - Navigate to `youtube.com/watch?v={id}`
   - Click "Save" button → select "Good music" playlist
   - Wait for confirmation, move to next
3. Add delays between actions to avoid rate limiting

### Implementation sketch

```python
# scripts/playlist_add.py
from playwright.sync_api import sync_playwright
import json
import time

PLAYLIST_NAME = "Good music"

def add_to_playlist(page, video_id: str):
    page.goto(f"https://www.youtube.com/watch?v={video_id}")
    page.wait_for_selector("button[aria-label='Save to playlist']")
    page.click("button[aria-label='Save to playlist']")

    # Wait for playlist popup
    page.wait_for_selector(f"text={PLAYLIST_NAME}")
    page.click(f"text={PLAYLIST_NAME}")

    time.sleep(1)  # Let it save

def main():
    with open("data/results.jsonl") as f:
        videos = [json.loads(line) for line in f]

    # Filter high/medium confidence
    videos = [v for v in videos if v["confidence"] in ("high", "medium")]

    with sync_playwright() as p:
        # Use persistent context to reuse login
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./chrome-profile",
            headless=False,  # Need to login first time
        )
        page = browser.new_page()

        for i, v in enumerate(videos):
            print(f"[{i+1}/{len(videos)}] Adding {v['video_id']}")
            try:
                add_to_playlist(page, v["video_id"])
            except Exception as e:
                print(f"  Error: {e}")
            time.sleep(2)  # Rate limit
```

### Setup steps

1. `uv add playwright && playwright install chromium`
2. Run script once with `headless=False` → login to YouTube manually
3. Re-run script → uses saved session

### Pros
- No API quota limits
- Full control over flow
- Can handle edge cases (already in playlist, etc.)

### Cons
- YouTube UI changes break selectors (maintenance burden)
- Slower (~3-5 sec per video)
- Needs visible browser (or careful headless setup)
- Risk of being flagged as bot if too fast

### Time estimate
- 700 videos × 4 sec = ~47 minutes
- With errors/retries: ~1-2 hours

---

## Option 3: Browser Userscript

### How it works

1. Install Tampermonkey/Violentmonkey
2. Load userscript that adds "Batch Import" button to YouTube
3. Paste video IDs → script clicks through playlist adds
4. Runs in your authenticated browser context

### Implementation sketch

```javascript
// ==UserScript==
// @name         YouTube Batch Playlist Add
// @match        https://www.youtube.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Add floating button
    const btn = document.createElement('button');
    btn.textContent = 'Batch Add';
    btn.style.cssText = 'position:fixed;top:10px;right:10px;z-index:9999;padding:10px;';
    document.body.appendChild(btn);

    btn.onclick = async () => {
        const input = prompt('Paste video IDs (one per line):');
        if (!input) return;

        const ids = input.trim().split('\n').filter(Boolean);

        for (const id of ids) {
            console.log(`Adding ${id}...`);

            // Navigate
            window.location.href = `https://www.youtube.com/watch?v=${id}`;
            await sleep(3000);

            // Click save button
            const saveBtn = document.querySelector('button[aria-label="Save to playlist"]');
            saveBtn?.click();
            await sleep(1000);

            // Click playlist checkbox
            const playlistItem = [...document.querySelectorAll('tp-yt-paper-checkbox')]
                .find(el => el.textContent.includes('Good music'));
            playlistItem?.click();
            await sleep(1000);
        }

        alert('Done!');
    };

    function sleep(ms) {
        return new Promise(r => setTimeout(r, ms));
    }
})();
```

### Better approach: iframe method

Instead of navigating away, open videos in hidden iframe or use YouTube's internal API:

```javascript
// Use YouTube's internal save endpoint (reverse-engineered)
async function addToPlaylist(videoId, playlistId) {
    const response = await fetch('https://www.youtube.com/youtubei/v1/browse/edit_playlist', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `SAPISIDHASH ${getSapisidHash()}`,
        },
        body: JSON.stringify({
            context: getYouTubeContext(),
            actions: [{
                addedVideoId: videoId,
                action: 'ACTION_ADD_VIDEO'
            }],
            playlistId: playlistId
        })
    });
    return response.json();
}
```

### Setup steps

1. Install Tampermonkey browser extension
2. Create new userscript, paste code
3. Navigate to YouTube, click "Batch Add"
4. Paste video IDs from `results.jsonl`

### Extracting video IDs for paste

```bash
# High confidence only
jq -r 'select(.confidence == "high") | .video_id' data/results.jsonl

# High + medium
jq -r 'select(.confidence == "high" or .confidence == "medium") | .video_id' data/results.jsonl
```

### Pros
- Runs in your real browser session (no bot detection)
- No external dependencies
- Quick to set up and iterate

### Cons
- Manual trigger (paste IDs)
- YouTube internal APIs may change
- Harder to track progress/errors
- Page navigation version is slow

---

## Comparison

| Aspect | Playwright | Userscript |
|--------|------------|------------|
| Setup complexity | Medium (install playwright) | Low (browser extension) |
| Maintenance | High (selectors break) | Medium (internal API changes) |
| Speed | ~4 sec/video | 1-3 sec/video (with internal API) |
| Reliability | Medium | Medium |
| Progress tracking | Easy (Python logging) | Manual |
| Bot detection risk | Higher | Lower |

## Recommendation

**For 700 videos one-time migration:**

1. Try **userscript with internal API** first - fastest if it works
2. Fall back to **Playwright** if internal API is blocked/complex
3. Do in batches of 50-100 to monitor for issues

**Next step:** Reverse-engineer YouTube's playlist add request in browser DevTools (Network tab) to see exact payload format.
