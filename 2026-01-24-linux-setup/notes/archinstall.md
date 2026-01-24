# Arch Linux Setup

## Installation

### Boot from USB

1. Create bootable USB with Ventoy (same as Windows setup)
2. Copy Arch ISO to Ventoy USB
3. Boot from USB (Dell: **F12** for boot menu, **F2** for BIOS)
4. Select Arch ISO in Ventoy

### archinstall

Run the guided installer:

```bash
archinstall
```

Walk through the menus:

| Setting | Value |
|---------|-------|
| Language | English |
| Mirrors | Select your region |
| Locales | `en_US.UTF-8` |
| Disk configuration | Best-effort default, ext4 or btrfs |
| Disk encryption | Skip (unless needed) |
| Bootloader | systemd-boot |
| Swap | True (zram) |
| Hostname | Pick a name |
| Root password | Skip (sudo user is enough) |
| User account | Create user, add to sudo/wheel |
| Profile | Desktop → GNOME |
| Audio | pipewire |
| Kernel | linux |
| Additional packages | `git base-devel` |
| Network | NetworkManager |
| Timezone | Your timezone |

After install completes, skip chroot and reboot. Remove USB when prompted.

## Post-install

### AUR helper

Install yay for AUR packages:

```bash
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
cd .. && rm -rf yay
```

### Development tools

Setup Homebrew (same as WSL):

```bash
# https://docs.brew.sh/Homebrew-on-Linux
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

brew install gh yazi
```

### Dotfiles

```bash
git clone https://github.com/hi-ogawa/dotfiles ~/code/personal/dotfiles
cd ~/code/personal/dotfiles
./sync.sh apply
```

### SSH and GitHub

```bash
ssh-keygen -t ed25519 -C <email>
# Add key to GitHub: https://github.com/settings/keys
gh auth login
```

## Desktop tips

- **Activities** - Super key or top-left corner
- **App launcher** - Super, then type app name
- **Window switching** - Alt+Tab (all), Alt+` (same app)
- **Workspaces** - Super+scroll or Super+PageUp/Down

## References

- [Arch Wiki - Installation guide](https://wiki.archlinux.org/title/Installation_guide)
- [Arch Wiki - archinstall](https://wiki.archlinux.org/title/Archinstall)
- [Arch Wiki - GNOME](https://wiki.archlinux.org/title/GNOME)
