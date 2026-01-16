# Research Notes

## ubi setup

ubi defaults to `./bin` (current directory), not `~/.local/bin`. Need to either:
1. Use `--in ~/.local/bin` every time
2. Add alias: `alias ubi='ubi --in ~/.local/bin'`

Install ubi itself:
```bash
curl -sSL https://raw.githubusercontent.com/houseabsolute/ubi/master/bootstrap/bootstrap-ubi.sh | TARGET=~/.local/bin sh
```

Usage:
```bash
ubi -p yt-dlp/yt-dlp -i ~/.local/bin
# or with alias:
ubi -p yt-dlp/yt-dlp
```

## Homebrew formula coverage

Checked `~/.local/bin` tools against Homebrew formulae API.

**In Homebrew (16):**
ast-grep, cloudflared, dagger, deno, duf, flyctl, gh, git-filter-repo, joshuto, lychee, opencode, poetry, qsv, ripgrep, yq, yt-dlp

**Not in Homebrew (3):**
- bun - has own installer (`curl -fsSL https://bun.sh/install | bash`)
- git-spr - niche tool
- claude - Anthropic CLI, too new

## Homebrew installation on Arch

```bash
# Prerequisites
sudo pacman -S base-devel curl git

# Install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to .bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
```

## Bootstrap problem

gh-bin requires Node to run (`npx gh-bin`), so on a fresh machine without Node it can't bootstrap itself.

Homebrew and ubi only need `curl | bash`:
```bash
# ubi
curl -sSL https://raw.githubusercontent.com/houseabsolute/ubi/master/bootstrap/bootstrap-ubi.sh | sh

# homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

This was the original motivation to look for alternatives when setting up a fresh WSL machine.

## Arch community sentiment on Homebrew

**Concerns:**
- Redundancy - "between repos and AUR, you can get almost anything"
- Fragmentation - tracking pacman + yay + Homebrew gets messy
- Dependency conflicts - Homebrew brings its own libs, can conflict with system (esp. CUDA/Python)
- Security theater - "no sudo" doesn't really help, malware can still access user data

**Pros:**
- Cross-platform consistency - same tools/versions across macOS and Linux
- Escape hatch - when AUR package is broken, Homebrew sometimes just works
- Familiarity - macOS converts already know it

**Pragmatic take:** Most Arch users say "unnecessary" but acknowledge it works. For single-binary CLI tools (not system libraries), the risk of conflicts is low.

Forum sources:
- https://forum.endeavouros.com/t/thoughts-on-homebrew-on-endeavouros/55141
- https://github.com/orgs/Homebrew/discussions/4503
- https://aur.archlinux.org/packages/brew-git

## Sources

- Homebrew install script: https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh
- Homebrew on Linux docs: https://docs.brew.sh/Homebrew-on-Linux
- Formula API used for check: `https://formulae.brew.sh/api/formula/{name}.json`
