# Local Audio → Streaming Migration

Moving from local audio file workflow (VLC + custom yt-dlp-like tool) to modern streaming service (YouTube Music).

## Background

Current setup:
- Desktop: YouTube + ublock for discovery/listening
- Custom desktop GUI app (yt-dlp-like) to download with proper metadata (artist, title, thumbnail)
- Mobile: VLC for commuting, browsing curated collection by artist

Target:
- YouTube Music Premium with Artists tab for organization
- Eliminates manual download/transfer workflow for mobile listening
- Artists tab organizes by channel name, which suffices for 99% of use cases

## Problem

YouTube Music has no batch import. Must add songs to library one-by-one. To migrate:
1. Need to map existing local audio files → original YouTube video IDs
2. Need to batch-add video IDs to YouTube Music library (no native feature)

## Files

- `plan.md` - Detailed planning, research, and progress
- `notes/` - Research findings
