<div align="center">

![Mainuan WebApp Manager Icon](assets/icons/128x128/org.mainuan.webappmanager.png)

# Mainuan WebApp Manager

[![License: GPL-3.0+](https://img.shields.io/badge/License-GPL--3.0%2B-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Version](https://img.shields.io/badge/version-1.0.1-green.svg)]()

**Mainuan WebApp Manager** is an elegant, lightweight Site Specific Browser (SSB) engine tailored for Mainuan Linux. It effortlessly turns any website into a standalone, desktop-integrated application utilizing isolated browser profiles for maximum privacy and separation from your primary web session.

WebApp integration manager for Mainuan Linux.

</div>

## Screenshots

<div align="center">
  <img src="assets/screenshots/screenshot1.png" width="30%" alt="Main Window"/>
  <img src="assets/screenshots/screenshot2.png" width="30%" alt="Add button"/>
  <img src="assets/screenshots/screenshot3.png" width="30%" alt="Creation Dialog"/>
</div>

## Features

- 🌐 **Multi-Engine Support**: Native or Flatpak versions of Firefox, Chrome, Chromium, Brave, Vivaldi, Edge, and Epiphany.
- ✏️ **Full WebApp Editing**: Reconfigure Name, URL, Icon, and Browser settings at any time without recreating the profile.
- ⚙️ **Extra Browser Parameters**: Add custom flags like `--start-maximized` or `--kiosk` with a new built-in help guide.
- 🔒 **Total Isolation & Incognito**: Generates sandboxed profiles and supports Incognito mode sessions.
- 🎨 **Mainuan UI Integration**: Official status bar with automatic detection of DE (Plasma) and protocol (Wayland/X11).
- 🧩 **No-UI Implementation**: Customized Firefox launch using `userChrome.css` and dynamic StartupWMClass mapping.
- 🤖 **Smart Favicons**: HD icons automatically downloaded via Google Favicon API. 
- 🌍 **Internationalization**: Ships translated out-of-the-box for `pt-PT, pt-BR, es, en, fr, de, it, ro, ru`.

## Requirements

- Python 3.10+
- GTK+ 3
- python3-gi
- At least one supported browser installed (native DEB/RPM or Flatpak).

## Installation

The Mainuan Webapp Manager is already installed on the Mainuan Linux ISO or available on the Mainuan Store.

On another Kubuntu/Ubuntu 26.04 system, download the `.deb` and the `SHA256SUMS` from
[latest release](https://github.com/mainuan/mainuan-webapp-manager/releases/latest),

```bash
sha256sum --check --ignore-missing SHA256SUMS
sudo apt install ./mainuan-webapp-manager_1.0.1.deb

```bash
git clone https://github.com/mainuan/mainuan-webapp-manager.git
cd mainuan-webapp-manager
python3 main.py
```
## Usage

Open **Mainuan Webapp Manager** from your application menu (under the System/Settings category) or run:

```bash
mainuan-webapp-manager
```

## 🆕 New in version 1.0.1 (November 17, 2026)

## Contributing

Report issues in [Issues](https://github.com/mainuan/mainuan-webapp-manager/issues)
and submit changes via pull request to the `main` branch. Every PR must pass the
[CI](https://github.com/mainuan/mainuan-webapp-manager/actions/workflows/ci.yml)
checks, which must all be green (passing). Document any visible changes in
[CHANGELOG.md](CHANGELOG.md) and `debian/changelog`.

## Créditos

- David Caixinha ([@tugatechlabDC](https://github.com/tugatechlabDC)): developer and maintainer of the package (`debian/control`).

This project is licensed under the GPL-3.0 License — see the `debian/copyright` file for details.

