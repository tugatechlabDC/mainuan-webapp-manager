"""
Visual theme for Mainuan AppImage Manager.

Uses the same palette and shapes as Mainuan Store, and follows the system
light/dark mode automatically (also while the app is running).
"""
import os
import re
import weakref
from string import Template

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GLib

DARK = {
    'bg': '#011a27', 'bg2': '#02232b', 'sidebar': '#010f15',
    'surface': '#032a35', 'banner': '#05505f', 'raised': '#053744', 'border': '#0b4857',
    'primary': '#08e2ea', 'primarySoft': '#3aeef3', 'primaryDark': '#0399b2',
    'onPrimary': '#012028', 'text': '#e8fbfd', 'dim': '#8fb8c0',
    'ok': '#3ddc97', 'warn': '#ffb454', 'err': '#ff7a7a', 'errSoft': '#ff9a9a',
    'onErr': '#2a0a0a',
    'shadow': 'rgba(0, 0, 0, 0.35)',
}
LIGHT = {
    'bg': '#f2f8fa', 'bg2': '#ffffff', 'sidebar': '#e2eef1',
    'surface': '#ffffff', 'banner': '#c4e8ee', 'raised': '#d9ecf0', 'border': '#bcd5db',
    'primary': '#02829a', 'primarySoft': '#0399b2', 'primaryDark': '#3aa5b8',
    'onPrimary': '#ffffff', 'text': '#0c2a33', 'dim': '#4b6770',
    'ok': '#1c8f5f', 'warn': '#b86e00', 'err': '#c93a3a', 'errSoft': '#d95555',
    'onErr': '#ffffff',
    'shadow': 'rgba(12, 42, 51, 0.18)',
}

_CSS = Template(r"""
/* ── Base ─────────────────────────────────────────────────────────── */
window, dialog, messagedialog, aboutdialog, .background {
    background-color: $bg;
    background-image: none;
    color: $text;
    font-size: 14px;
}

label.dim-label, .dim-label { color: $dim; opacity: 1; }
label.mn-title { font-size: 15px; font-weight: 700; }
label.mn-sub { font-size: 12px; color: $dim; }
label.mn-empty { font-size: 15px; color: $dim; }
label selection, entry selection, textview text selection, .view selection {
    background-color: $primaryDark; color: #ffffff;
}
*:link, link, label link { color: $primary; }
*:link:hover, link:hover { color: $primarySoft; }
separator { background-color: $border; background-image: none; min-width: 1px; min-height: 1px; }

/* ── Title bar (window buttons on the right) ──────────────────────── */
headerbar, .titlebar {
    background-image: none;
    background-color: $sidebar;
    color: $text;
    border: none;
    border-bottom: 1px solid $border;
    box-shadow: none;
    min-height: 52px;
    padding: 0 10px;
}
headerbar .title, headerbar label.mn-hdr-title { color: $text; font-size: 16px; font-weight: 700; }
headerbar .subtitle { color: $dim; font-size: 12px; }
headerbar button {
    background-color: $raised; border-color: transparent; padding: 6px 10px;
}
headerbar button:hover { background-color: $banner; }
headerbar button.mn-wbtn {
    background-image: none;
    background-color: transparent;
    border: none;
    box-shadow: none;
    border-radius: 10px;
    min-width: 34px;
    min-height: 34px;
    padding: 0;
    margin: 0 2px;
}
headerbar button.mn-wbtn:hover { background-color: $raised; }
headerbar button.mn-wbtn:active { background-color: $border; }
headerbar button.mn-wbtn.mn-close:hover { background-color: $err; }
headerbar button.mn-wbtn.mn-close:active { background-color: $errSoft; }

/* ── Buttons ──────────────────────────────────────────────────────── */
button {
    background-image: none;
    background-color: transparent;
    color: $text;
    border: 1px solid $border;
    border-radius: 10px;
    padding: 6px 18px;
    min-height: 24px;
    box-shadow: none;
    text-shadow: none;
    font-weight: 600;
}
button:hover { background-color: $raised; background-image: none; }
button:active, button:checked { background-color: $border; background-image: none; }
button:disabled { opacity: 0.5; }
button:focus { border-color: $primary; }
button.suggested-action {
    background-color: $primary; color: $onPrimary; border-color: transparent;
}
button.suggested-action:hover { background-color: $primarySoft; }
button.suggested-action:active { background-color: $primaryDark; }
button.destructive-action {
    background-color: $err; color: $onErr; border-color: transparent;
}
button.destructive-action:hover { background-color: $errSoft; }
button.destructive-action:active { background-color: $err; }
button.mn-icon {
    padding: 6px; min-width: 22px; min-height: 22px;
    background-color: $raised; border-color: transparent;
}
button.mn-icon:hover { background-color: $banner; }
button.mn-icon.destructive-action { background-color: $raised; color: $err; }
button.mn-icon.destructive-action:hover { background-color: $err; color: $onErr; }

/* ── Entries ──────────────────────────────────────────────────────── */
entry, spinbutton, combobox button.combo {
    background-image: none;
    background-color: $surface;
    color: $text;
    border: 1px solid $border;
    border-radius: 10px;
    padding: 6px 12px;
    min-height: 24px;
    box-shadow: none;
    caret-color: $primary;
}
entry:focus, spinbutton:focus { border-color: $primary; box-shadow: none; }
entry:disabled { opacity: 0.55; }

/* ── Cards (list rows) ────────────────────────────────────────────── */
list { background-color: transparent; background-image: none; color: $text; }
list.mn-cards { padding: 6px 8px; }
list.mn-cards row {
    background-color: $surface;
    color: $text;
    border: 1px solid $border;
    border-radius: 12px;
    margin: 4px 6px;
    padding: 0;
}
list.mn-cards row:hover { background-color: $raised; }
list.mn-cards row:focus { background-color: $surface; color: $text; }
list.mn-cards row:selected { background-color: $raised; color: $text; border-color: $primary; }
list.mn-cards row:selected:hover { background-color: $raised; }

scrolledwindow, scrolledwindow viewport, viewport { background-color: transparent; background-image: none; }
scrolledwindow { border: none; }
scrolledwindow.frame { border: 1px solid $border; border-radius: 10px; }
textview, textview text, .view, iconview {
    background-color: $surface; color: $text;
}
textview text { background-color: $surface; }
treeview.view { background-color: $surface; color: $text; }
treeview.view:selected, .view:selected, row:selected, iconview:selected {
    background-color: $primaryDark; color: #ffffff;
}
treeview header button {
    background-color: $raised; color: $text; border-radius: 0; border-width: 0 0 1px 0;
    border-color: $border; padding: 6px 10px;
}
placessidebar, placessidebar list, .sidebar { background-color: $sidebar; color: $text; }
placessidebar row:selected { background-color: $raised; color: $primary; }

/* ── Scrollbars ───────────────────────────────────────────────────── */
scrollbar { background-color: transparent; background-image: none; border: none; }
scrollbar trough { background-color: transparent; border: none; }
scrollbar slider {
    min-width: 8px; min-height: 30px;
    border-radius: 8px;
    background-color: $border;
    border: 2px solid transparent;
    background-clip: padding-box;
}
scrollbar slider:hover { background-color: $primaryDark; }
scrollbar slider:active { background-color: $primary; }
scrollbar button { min-width: 0; min-height: 0; padding: 0; border: none; background: none; }

/* ── Switch / check ───────────────────────────────────────────────── */
switch {
    background-image: none;
    background-color: $border;
    color: $dim;
    border: 1px solid $border;
    border-radius: 15px;
    min-width: 48px;
    min-height: 26px;
    box-shadow: none;
    text-shadow: none;
}
switch:checked { background-color: $primary; color: $onPrimary; border-color: $primary; }
switch slider {
    background-image: none;
    background-color: #ffffff;
    border: none;
    border-radius: 12px;
    min-width: 22px;
    min-height: 22px;
    margin: 1px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.35);
}
check, radio {
    background-image: none;
    background-color: $surface;
    color: $onPrimary;
    border: 1px solid $border;
    border-radius: 6px;
    min-width: 18px; min-height: 18px;
    box-shadow: none;
}
radio { border-radius: 100px; }
check:checked, radio:checked, check:indeterminate {
    background-color: $primary; border-color: $primary; color: $onPrimary;
}
check:hover, radio:hover { border-color: $primary; }

/* ── Progress / spinner ───────────────────────────────────────────── */
progressbar trough {
    background-image: none; background-color: $raised; border: none;
    border-radius: 8px; min-height: 16px; box-shadow: none;
}
progressbar progress {
    background-image: none; background-color: $primary; border: none;
    border-radius: 8px; min-height: 16px; box-shadow: none;
}
progressbar { color: $text; font-size: 11px; font-weight: 600; }
spinner { color: $primary; }

/* ── Tooltips / menus / popovers ──────────────────────────────────── */
tooltip, tooltip.background {
    background-color: $raised; background-image: none; color: $text;
    border: 1px solid $border; border-radius: 8px; box-shadow: none;
}
tooltip decoration { box-shadow: none; }
tooltip label { color: $text; }
menu, .menu, popover, popover.background {
    background-color: $surface; color: $text;
    border: 1px solid $border; border-radius: 10px;
}
menuitem, modelbutton { color: $text; }
menuitem:hover, modelbutton:hover { background-color: $raised; }

/* ── Dialogs ──────────────────────────────────────────────────────── */
dialog .dialog-action-area, messagedialog .dialog-action-area { padding: 8px 12px 12px 12px; }
dialog .dialog-action-area button, messagedialog .dialog-action-area button { margin: 0 4px; }
messagedialog .titlebar, dialog .titlebar { background-color: $sidebar; }
stackswitcher button {
    border-radius: 100px; padding: 4px 16px; min-height: 22px;
    background-color: transparent; border: 1px solid $border; font-weight: 500;
}
stackswitcher button:hover { background-color: $raised; }
stackswitcher button:checked { background-color: $primary; color: $onPrimary; border-color: $primary; }

/* ── Status bar ───────────────────────────────────────────────────── */
.mn-status { background-color: $sidebar; border-top: 1px solid $border; }
.mn-status label { color: $dim; font-size: 12px; }
""")

# Old hard-coded markup colours → palette keys (so labels follow light/dark)
_MARKUP_COLORS = {
    '#08c8d0': 'primary', '#4ec94e': 'ok', '#4ec9b0': 'ok',
    '#888888': 'dim', '#666666': 'dim', '#ff4444': 'err',
}
_MARKUP_RE = re.compile('|'.join(re.escape(k) for k in _MARKUP_COLORS), re.I)

_redraw = weakref.WeakSet()
_state = {'dark': True, 'provider': None, 'window_cbs': [], 'portal_ok': True}


def palette(dark=None):
    return DARK if (_state['dark'] if dark is None else dark) else LIGHT


def color(name):
    return palette()[name]


def colorize(markup):
    """Swap legacy fixed colours in Pango markup for the active palette."""
    pal = palette()
    return _MARKUP_RE.sub(lambda m: pal[_MARKUP_COLORS[m.group(0).lower()]], markup)


def _patch_label_markup():
    original = Gtk.Label.set_markup
    if getattr(original, '_mn_patched', False):
        return

    def set_markup(self, markup):
        return original(self, colorize(markup))
    set_markup._mn_patched = True
    Gtk.Label.set_markup = set_markup


# ── System dark/light detection ──────────────────────────────────────────────

def _portal_color_scheme():
    """freedesktop portal: 1 = dark, 2 = light, 0 = no preference."""
    if not _state['portal_ok']:
        return None
    try:
        bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        res = bus.call_sync(
            'org.freedesktop.portal.Desktop', '/org/freedesktop/portal/desktop',
            'org.freedesktop.portal.Settings', 'Read',
            GLib.Variant('(ss)', ('org.freedesktop.appearance', 'color-scheme')),
            None, Gio.DBusCallFlags.NONE, 300, None)
        val = res.unpack()[0]
        while isinstance(val, GLib.Variant):
            val = val.unpack()
        val = int(val)
        if val == 1:
            return True
        if val == 2:
            return False
        return None
    except Exception:
        _state['portal_ok'] = False
        return None


def _kde_is_dark():
    path = os.path.join(os.environ.get('XDG_CONFIG_HOME') or os.path.expanduser('~/.config'),
                        'kdeglobals')
    try:
        section = ''
        scheme = ''
        rgb = None
        with open(path, encoding='utf-8', errors='ignore') as fh:
            for line in fh:
                line = line.strip()
                if line.startswith('['):
                    section = line
                elif section == '[General]' and line.startswith('ColorScheme='):
                    scheme = line.split('=', 1)[1]
                elif section == '[Colors:Window]' and line.startswith('BackgroundNormal='):
                    parts = line.split('=', 1)[1].split(',')
                    rgb = [int(p) for p in parts[:3]]
        if rgb:
            lum = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
            return lum < 128
        if scheme:
            return 'dark' in scheme.lower()
    except Exception:
        pass
    return None


def _gsettings_is_dark():
    try:
        src = Gio.SettingsSchemaSource.get_default()
        if src and src.lookup('org.gnome.desktop.interface', True):
            s = Gio.Settings.new('org.gnome.desktop.interface')
            scheme = s.get_string('color-scheme')
            if scheme == 'prefer-dark':
                return True
            if scheme == 'prefer-light':
                return False
            if 'dark' in s.get_string('gtk-theme').lower():
                return True
    except Exception:
        pass
    return None


def _gtk_settings_is_dark():
    try:
        st = Gtk.Settings.get_default()
        name = (st.get_property('gtk-theme-name') or '').lower()
        if 'dark' in name:
            return True
        if name:
            return False
    except Exception:
        pass
    return None


def system_is_dark():
    hint = os.environ.get('MAINUAN_THEME_TYPE', '').lower()
    if hint in ('dark', 'light'):
        return hint == 'dark'
    for probe in (_portal_color_scheme, _kde_is_dark, _gsettings_is_dark,
                  _gtk_settings_is_dark):
        res = probe()
        if res is not None:
            return res
    return True


# ── Apply ────────────────────────────────────────────────────────────────────

def apply(dark):
    """Load the CSS for the given mode on the whole screen (all windows/dialogs)."""
    _state['dark'] = bool(dark)
    screen = Gdk.Screen.get_default()
    if screen is None:
        return
    try:
        settings = Gtk.Settings.get_default()
        settings.set_property('gtk-application-prefer-dark-theme', bool(dark))
        settings.set_property('gtk-decoration-layout', ':minimize,maximize,close')
    except Exception:
        pass
    provider = _state['provider']
    if provider is None:
        provider = Gtk.CssProvider()
        _state['provider'] = provider
        Gtk.StyleContext.add_provider_for_screen(
            screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION + 1)
    css = _CSS.substitute(palette(dark))
    try:
        provider.load_from_data(css.encode('utf-8'))
    except GLib.Error as exc:  # pragma: no cover
        print(f'Theme CSS error: {exc.message}')
    for w in list(_redraw):
        try:
            w.queue_draw()
        except Exception:
            pass
    for cb in list(_state['window_cbs']):
        try:
            cb(bool(dark))
        except Exception:
            pass


def register_redraw(widget):
    """Widget that must be redrawn when the theme switches (self-drawn icons)."""
    _redraw.add(widget)


def on_change(callback):
    """Register callback(dark) to run after the theme switches."""
    _state['window_cbs'].append(callback)


def start():
    """Apply the system theme now and keep following it while the app runs."""
    _patch_label_markup()
    apply(system_is_dark())

    def refresh(*_args):
        dark = system_is_dark()
        if dark != _state['dark']:
            apply(dark)
        return GLib.SOURCE_CONTINUE

    # Instant reaction on desktops that emit the portal signal…
    try:
        bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        bus.signal_subscribe(
            'org.freedesktop.portal.Desktop', 'org.freedesktop.portal.Settings',
            'SettingChanged', '/org/freedesktop/portal/desktop', None,
            Gio.DBusSignalFlags.NONE, lambda *_a: GLib.idle_add(refresh))
    except Exception:
        pass
    # …and a light safety-net poll for everything else.
    GLib.timeout_add_seconds(3, refresh)
    try:
        st = Gtk.Settings.get_default()
        st.connect('notify::gtk-theme-name', refresh)
        st.connect('notify::gtk-application-prefer-dark-theme', lambda *_a: None)
    except Exception:
        pass
