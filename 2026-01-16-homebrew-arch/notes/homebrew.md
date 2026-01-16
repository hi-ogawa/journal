# Homebrew Architecture

## Installation location

`/home/linuxbrew/.linuxbrew` is just a directory, not a Unix user.

The path looks like a home directory but there's no `linuxbrew` user - it's a fixed location Homebrew chose for Linux. Everything is owned by your user.

| Platform | Location | Reason |
|----------|----------|--------|
| macOS Intel | `/usr/local` | Traditional Unix location |
| macOS ARM | `/opt/homebrew` | Apple's requirement for ARM |
| Linux | `/home/linuxbrew/.linuxbrew` | Avoid conflicts with system `/usr/local` |

## Directory structure

```
/home/linuxbrew/.linuxbrew/
├── bin/          → symlinks to executables
├── lib/          → symlinks to libraries
├── include/      → symlinks to headers
├── opt/          → symlinks to "current" version in Cellar
├── Cellar/       → actual installed packages (versioned)
├── Caskroom/     → GUI apps (mostly macOS)
├── Homebrew/     → brew itself (Git repo)
└── var/homebrew/linked → tracking what's linked
```

## How package install works

```bash
brew install ripgrep
```

1. Downloads/extracts to `Cellar/ripgrep/14.1.0/bin/rg`
2. Creates symlink: `opt/ripgrep` → `Cellar/ripgrep/14.1.0`
3. Creates symlink: `bin/rg` → `../Cellar/ripgrep/14.1.0/bin/rg`

This symlink-based approach allows:
- Multiple versions in Cellar simultaneously
- Easy switching between versions
- Clean uninstall (just remove from Cellar, update symlinks)

## Sudo usage

- `sudo` is used ONCE during install to create `/home/linuxbrew/.linuxbrew` with your ownership
- After that, everything is user-writable
- Day-to-day `brew install` needs no sudo

## What gets cloned during install

The install script clones https://github.com/Homebrew/brew to `/home/linuxbrew/.linuxbrew/Homebrew/`:

```
Homebrew/
├── Library/    → the actual brew code (Ruby)
├── bin/        → brew executable
├── docs/       → documentation
├── completions/→ shell completions
└── .git/       → full git history (~320k objects)
```

The formulae (package definitions) live in a separate repo `homebrew/homebrew-core` that gets cloned lazily on first `brew install`. It goes to:
```
/home/linuxbrew/.linuxbrew/Homebrew/Library/Taps/homebrew/homebrew-core/
```

## Portable Ruby

Homebrew itself is written in Ruby. It downloads its own Ruby (`portable-ruby-3.4.8.x86_64_linux.bottle.tar.gz`) to avoid depending on system Ruby - part of the "bring your own dependencies" philosophy.

## Build dependencies (base-devel, gcc)

Homebrew suggests installing `base-devel` and `brew install gcc` for building packages from source.

**On Arch, probably skip both:**
- Arch has fresh system gcc (rolling release)
- Single-binary CLI tools all have bottles (no compilation)
- Mixing Homebrew's gcc with system = ABI conflicts
- If a specific package needs source build, deal with it then

The recommendation is aimed at old distros (Ubuntu LTS, CentOS) with outdated compilers, not Arch.

## PATH priority

`brew shellenv` **prepends** Homebrew's bin to PATH:
```bash
PATH="/home/linuxbrew/.linuxbrew/bin:...${PATH}"
```

This means Homebrew binaries take priority over system ones.

**Mitigated by:**
- Homebrew gcc uses versioned names (`gcc-15`, not `gcc`) - no shadow
- CLI tools (ripgrep, yt-dlp) have unique names - no system equivalents

**Watch out for:**
- Installing same tool via both Homebrew and pacman
- Formulas that install common binary names

## Bottle infrastructure

### What's a bottle

Prebuilt binary tarball, so users don't compile from source:
```
ripgrep-14.1.0.x86_64_linux.bottle.tar.gz
├── ripgrep/
│   └── 14.1.0/
│       ├── bin/rg
│       ├── share/...
│       └── .brew/ripgrep.rb   ← formula embedded
```

Filename encodes: name, version, architecture, OS.

### Where bottles are hosted

**GitHub Packages** (Container Registry):
```
ghcr.io/v2/homebrew/core/<formula>/blobs/sha256:...
```

Example from install output:
```
==> Downloading https://ghcr.io/v2/homebrew/core/portable-ruby/blobs/sha256:63a9c333...
```

### Build pipeline

```
PR to homebrew/homebrew-core
    ↓
BrewTestBot (GitHub Actions)
    ↓
setup_runners job
    ↓
tests job (parallel matrix)
    ├── macOS Intel
    ├── macOS ARM
    └── Linux x86_64 (Ubuntu container)
    ↓
All pass → bottles uploaded to ghcr.io
    ↓
Formula updated with bottle checksums
    ↓
Merged
```

**Linux is first-class:** Single workflow file, parallel matrix jobs, both platforms must pass to merge. Not a separate pipeline or afterthought.

This changed in 2019 when "Linuxbrew" merged upstream into Homebrew proper.

### Security

Bottles have **build provenance** via Sigstore - cryptographic attestation that the bottle was built by Homebrew's official CI, not tampered with.

## Dependency considerations

Some tools pull many dependencies (e.g., `deno` pulls sqlite, zlib, libffi, ncurses, etc.). These are Homebrew's own copies, not system libraries.

**Check before installing:**
```bash
brew info <package>  # look at "Required:" section
```

**For tools with many deps:** GitHub releases via gh-bin/ubi may be better - upstream builds are typically more self-contained.

**Good news:** Uninstall is clean - `brew uninstall` autoremoving unused deps:
```
$ brew uninstall deno
Uninstalling deno...
==> Autoremoving 11 unneeded formulae:
jpeg-turbo, libffi, libtiff, little-cms2, lz4, ncurses, readline, sqlite, xz, zlib, zstd
```

## Sources

- https://docs.brew.sh/Homebrew-on-Linux
- https://docs.brew.sh/Formula-Cookbook (explains Cellar structure)
- https://github.com/Homebrew/brew/blob/master/docs/Bottles.md
- https://blog.trailofbits.com/2024/05/14/a-peek-into-build-provenance-for-homebrew/
