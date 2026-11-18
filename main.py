#!/usr/bin/env python3
import sys
import os
import signal
import gettext
import locale
from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk, GdkPixbuf, Gio

# Basic configuration
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
LOCALE_DIR = PROJECT_ROOT / "locale"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Desktop integration for all DEs (X11 + Wayland)
GLib.set_prgname('org.mainuan.webappmanager')
GLib.set_application_name('mainuan-webapp-manager')
Gtk.Window.set_default_icon_name('org.mainuan.webappmanager')
if hasattr(Gdk, 'set_program_class'):
    Gdk.set_program_class('org.mainuan.webappmanager')

# Internationalization: the UI language always follows the system language
def _system_languages():
    """System language preference list, most specific first (e.g. pt_BR, pt)."""
    names = []
    for raw in GLib.get_language_names():
        name = raw.split('.')[0].split('@')[0].replace('-', '_')
        if name and name not in ('C', 'POSIX') and name not in names:
            names.append(name)
    return names


def _setup_translation():
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        pass
    gettext.bindtextdomain('mainuan-webapp-manager', str(LOCALE_DIR))
    gettext.textdomain('mainuan-webapp-manager')
    translation = gettext.translation(
        'mainuan-webapp-manager', str(LOCALE_DIR),
        languages=_system_languages() or None, fallback=True)
    return translation.gettext


_ = _setup_translation()

from core.browser_manager import BrowserManager
from core.webapp_manager import WebAppManager
from ui.main_window import MainWindow
from utils.environment import get_environment_detector
from ui import theme as mn_theme


class MainuanWebAppManagerApplication(Gtk.Application):
    """Main application class using Gtk.Application for proper Wayland/X11 integration."""
    
    def __init__(self):
        super().__init__(
            application_id='org.mainuan.webappmanager',
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.app_path = PROJECT_ROOT
        self.assets_path = ASSETS_DIR
        self.window = None # Changed from self.main_window
        
        # Connect signals
        self.connect('startup', self.on_startup)
        self.connect("activate", self.on_activate)
        self.connect("shutdown", self.on_shutdown)
        
        # Initialize environment detector
        self.environment_detector = get_environment_detector()
        
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)
    
    def _handle_signal(self, signum, frame):
        self.quit()
    
    def on_startup(self, app):
        # Mainuan look; follows the system light/dark mode automatically
        mn_theme.start()
        print(_("Starting Mainuan WebApp Manager..."))
        self.browser_manager = BrowserManager()
        self.webapp_manager = WebAppManager(self.browser_manager)

        about_action = Gio.SimpleAction.new('about', None)
        about_action.connect('activate', lambda *_: self.window._show_about() if self.window else None)
        self.add_action(about_action)
    
    def on_activate(self, app):
        if self.window: # Changed from self.main_window
            self.window.present() # Changed from self.main_window
            return
            
        # from ui.main_window import MainWindow # This line is removed as it's now a top-level import
        if not self.window:
            self.window = MainWindow(self, self.browser_manager, self.webapp_manager, self.environment_detector, _, self.assets_path)
            self.window.show_all()
    
    def on_shutdown(self, app):
        print(_("Shutting down Mainuan WebApp Manager..."))
        self._cleanup_garbage()
    
    def _cleanup_garbage(self):
        """Remove __pycache__ and other temporary files."""
        try:
            import shutil
            for root, dirs, files in os.walk(self.app_path):
                if '__pycache__' in dirs:
                    pycache_path = os.path.join(root, '__pycache__')
                    try:
                        shutil.rmtree(pycache_path, ignore_errors=True)
                    except Exception:
                        pass
        except Exception as e:
            print(_("Cleanup warning: {}").format(e))


def main():
    app = MainuanWebAppManagerApplication()
    return app.run(sys.argv)

if __name__ == '__main__':
    sys.exit(main())