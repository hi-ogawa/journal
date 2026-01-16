# Plan

## Homebrew setup

- [x] Run Homebrew installer
- [x] Add shellenv to `.bashrc` (already had it from WSL)

## Replace ~/.local/bin with Homebrew

**In Homebrew (can migrate):**
- [x] ast-grep
- [ ] cloudflared
- [ ] dagger
- [ ] deno
- [x] duf
- [ ] fly → `brew install flyctl`
- [x] gh
- [ ] git-filter-repo
- [ ] joshuto
- [ ] lychee
- [ ] opencode
- [ ] poetry
- [ ] qsv
- [ ] rg → `brew install ripgrep`
- [ ] yq
- [ ] yt-dlp

**Not in Homebrew (keep as-is):**
- bun / bunx - official installer
- claude - official installer
- git-spr - gh-bin or ubi
- edge-playback / edge-tts - pip packages?

## After migration

- Remove migrated binaries from `~/.local/bin`
- Test everything works

## Optional / later

- [ ] Enable bash completions for brew + installed tools (shellenv doesn't set this up)
