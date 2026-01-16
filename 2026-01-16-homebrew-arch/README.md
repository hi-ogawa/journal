# CLI Binary Management on Arch Linux

Finding a maintained alternative to `gh-bin` for installing single-binary CLI tools.

## Background

I made `gh-bin` to one-shot install CLI binaries from GitHub releases to `~/.local/bin`. It's a thin hack that works surprisingly well, but I don't want to maintain it.

The pattern it solves: many dev CLI tools suggest `curl | bash` installation, dropping a binary into local/bin. I wanted something cleaner.

**gh-bin's pragmatic assumptions**:
- Always install to `~/.local/bin` - convenient but general-purpose tools need path flexibility
- Requires Node runtime - can't bootstrap itself on a fresh machine (this was the original motivation to find alternatives when setting up WSL)

**Prior experience**: Scoop on Windows native was a good experience (user-space CLI tools, no admin). Moving to WSL, Homebrew is the closest equivalent.

## Options

| Tool | What it is | Tradeoff |
|------|------------|----------|
| **ubi** | Direct GitHub/GitLab binary downloader | No install tracking, need `--in` flag |
| **Homebrew** | Full package manager | Heavier, but has upgrade tracking + huge ecosystem |
| **mise + ubi** | mise uses ubi as backend | Adds tracking layer, `mise upgrade` works |
| **aqua** | Declarative CLI version manager | Smaller registry than Homebrew |

## Decision

**Homebrew** - covers 90% of needs with trusted ecosystem. Minor itches acceptable.

For the remaining 10% (tools not in Homebrew): ubi or official installers.

## Sources

- gh-bin (my tool): https://github.com/hi-ogawa/js-utils/tree/main/packages/gh-bin
- ubi: https://github.com/houseabsolute/ubi
- Homebrew on Linux: https://docs.brew.sh/Homebrew-on-Linux
- Formula search: https://formulae.brew.sh/
- mise (with ubi backend): https://mise.jdx.dev/
- aqua: https://aquaproj.github.io/
