# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/lang/en/).

## [1.0.1] - 2026-11-14

### 🎨 Changed
- New round application icon (Mainuan teal with a web globe), installed in every hicolor size.
- Interface restyled like the other Mainuan apps: same palette, rounded cards, buttons and fields. Functions and menus are unchanged.
- Light and dark themes follow the system automatically (also while the app is open). Button icons are drawn by the app, so they are always visible.
- Title bar with the logo and the MINIMIZE, MAXIMIZE and CLOSE buttons on the right.
- Language always follows the system language (pt_BR, pt, en, es, fr, de, it, ro, ru); there is no language selector in the app.

## [1.0.0-5] - 2026-07-07

### 🔧 Changed
- Build dependency `python3-all` replaced with `python3`.

---

## [1.0.0-4] - 2026-04-30

### 💄 Changed
- Simplified the footer UI text to match the modern Mainuan standard layout (`XFCE · X11`).

### 🔧 Fixed
- **Icon Persistence**: WebApp icons are now saved permanently in the local data folder instead of the cache folder, preventing icon loss during system cleanups.
- **Theme Support**: Fixed dark mode being forced on light themes; the application now correctly respects the system's light or dark GTK theme preference.

---

## [1.0.0-3] - 2026-03-22

### 🔧 Fixed
- **UI colors**: Fixed background color inconsistency — window, list and scrolled area now consistently use the correct Mainuan dark theme color (#2b2b2b).

---

## [1.0.0-2] - 2026-03-21

### ✨ Added
- **About dialog**: Press F1 or use the GNOME application menu to open the About dialog with version, author, license and website.

---

## [1.0.0-1] - 2026-03-10

### ✨ Standardized Mainuan UI
- **Official Mainuan Footer**: Implemented an official status bar following the Mainuan ecosystem standard.
- **Environment Detection**: Added automatic identification of Desktop Environment (GNOME, Plasma, XFCE) and Protocol (Wayland, X11).
- **Incognito Mode**: New support for private browsing sessions with fully isolated profiles.
- **Extended Parameters Help**: Added a comprehensive guide for advanced browser flags and parameters.
- **UI Alignment**: Consistent use of `dim-label` styling and standard margins (15, 15, 8, 8) for seamless transition between Mainuan apps.

## [1.0.0] - 2026-03-04

### 🎉 Initial Release
- **Full WebApp Editing**: Users can now edit Name, URL, Icon, Browser, and Navigation Bar settings for existing WebApps.
- **Extra Browser Parameters**: Support for custom browser flags (e.g., `--start-maximized`, `--kiosk`) both at creation and editing.
- **Improved Wayland Compatibility**: Enhanced icon mapping and window association for KDE Plasma 6 and other modern environments.
- **Independent Firefox Instances**: Optimized Firefox SSB behavior with truly isolated processes and dedicated icons.
- **Smart Favicons**: Fallback mechanism to natively download high-quality website icons via Google Favicons API.
- **Full Internationalization (i18n)**: Translation ready for the 8 default languages in Mainuan Linux.

---

## Types of Changes

- **Added** for new features
- **Improved** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for removed features
- **Fixed** for bug fixes
- **Security** for vulnerabilities

## Author

Developed and maintained by David Caixinha

