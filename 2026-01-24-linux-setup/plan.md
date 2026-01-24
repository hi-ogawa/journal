# Plan

## Current State

**dotfiles repo** (`~/code/personal/dotfiles`):
- `sync.sh` - handles Linux/WSL/Windows config sync
- Configs: `.bashrc`, `.gitconfig`, vscode, claude, opencode
- Arch setup guide is minimal (links to old gists)

**windows-setup repo** (`~/code/personal/windows-setup`):
- Comprehensive `setup.md` guide for Windows + WSL
- Good reference for the level of detail we want

## Goal

Create a comprehensive Arch Linux setup guide in dotfiles, similar to windows-setup quality.

## Decisions

- **DE**: GNOME
- **Disk**: Arch-only (purge Windows)
- **Hardware**: Laptop (Dell)
- **Install method**: archinstall
- **Tooling**: Homebrew (consistent with WSL setup)
- **Config**: dotfiles repo with sync.sh

## Checklist

- [x] Document Arch installation process (archinstall)
- [ ] Post-install essentials
  - [ ] AUR helper (yay)
  - [ ] Homebrew
- [ ] Development tools
  - [ ] gh, yazi
  - [ ] Node.js (volta/fnm)
  - [ ] Editors (vscode)
- [ ] Apply dotfiles
- [ ] Extend sync.sh if needed for Arch-specific configs

## Notes

Reference external sources:
- Arch Wiki (primary)
- Existing gist: https://gist.github.com/hi-ogawa/a873d9406f580dfdf1e391a427a4dd0b
