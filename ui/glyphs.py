"""
Self-drawn icon buttons (cairo). They do not depend on the system icon theme,
so they are always visible and always use the app palette (light or dark).
"""
import math

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from ui import theme as mn_theme


def _line(cr, pts, close=False):
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    if close:
        cr.close_path()


def draw_glyph(cr, name, rgb, maximized=False):
    """Draw glyph `name` in a 16x16 box (cairo context already translated)."""
    cr.set_source_rgba(*rgb)
    cr.set_line_width(1.7)
    cr.set_line_cap(1)    # round
    cr.set_line_join(1)   # round
    if name == 'minimize':
        _line(cr, [(3, 11.5), (13, 11.5)]); cr.stroke()
    elif name == 'maximize':
        if maximized:
            _line(cr, [(3, 6), (10, 6), (10, 13), (3, 13)], close=True); cr.stroke()
            _line(cr, [(6, 6), (6, 3), (13, 3), (13, 10), (10, 10)]); cr.stroke()
        else:
            _line(cr, [(3, 3), (13, 3), (13, 13), (3, 13)], close=True); cr.stroke()
    elif name == 'close':
        _line(cr, [(3.5, 3.5), (12.5, 12.5)]); cr.stroke()
        _line(cr, [(12.5, 3.5), (3.5, 12.5)]); cr.stroke()
    elif name == 'plus':
        _line(cr, [(8, 3), (8, 13)]); cr.stroke()
        _line(cr, [(3, 8), (13, 8)]); cr.stroke()
    elif name == 'props':
        for y in (4.5, 8, 11.5):
            _line(cr, [(3, y), (13, y)]); cr.stroke()
    elif name == 'update':
        cr.arc(8, 8, 5, math.radians(40), math.radians(340)); cr.stroke()
        _line(cr, [(13.7, 9.1), (14.77, 5.55), (10.63, 7.05)], close=True); cr.fill()
    elif name == 'minus':
        _line(cr, [(3, 8), (13, 8)]); cr.stroke()
    elif name == 'edit':
        _line(cr, [(3, 13), (3.6, 10.2), (10.8, 3), (13, 5.2), (5.8, 12.4)], close=True); cr.stroke()
        _line(cr, [(9.2, 4.6), (11.4, 6.8)]); cr.stroke()
    elif name == 'help':
        cr.arc(8, 8, 6, 0, 2 * math.pi); cr.stroke()
        _line(cr, [(8, 7.2), (8, 11.4)]); cr.stroke()
        cr.arc(8, 4.9, 0.55, 0, 2 * math.pi); cr.fill()
    elif name == 'play':
        _line(cr, [(5, 3), (13, 8), (5, 13)], close=True); cr.fill()
    elif name == 'trash':
        _line(cr, [(3, 4.5), (13, 4.5)]); cr.stroke()
        _line(cr, [(6.5, 4.5), (6.5, 3), (9.5, 3), (9.5, 4.5)]); cr.stroke()
        _line(cr, [(4.5, 6.5), (5.3, 13), (10.7, 13), (11.5, 6.5)]); cr.stroke()
        _line(cr, [(7, 8), (7, 11)]); cr.stroke()
        _line(cr, [(9, 8), (9, 11)]); cr.stroke()


def _rgba(hexcolor):
    h = hexcolor.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)


class GlyphButton(Gtk.Button):
    """Button showing a self-drawn glyph that follows the app palette."""

    def __init__(self, glyph, size=16):
        super().__init__()
        self.glyph = glyph
        self.maximized = False
        self._hover = False
        self._size = size
        self.area = Gtk.DrawingArea()
        self.area.set_size_request(size, size)
        self.area.set_halign(Gtk.Align.CENTER)
        self.area.set_valign(Gtk.Align.CENTER)
        self.area.connect('draw', self._on_draw)
        self.add(self.area)
        self.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)
        self.connect('enter-notify-event', self._set_hover, True)
        self.connect('leave-notify-event', self._set_hover, False)
        self.connect('state-flags-changed', lambda *_a: self.area.queue_draw())
        mn_theme.register_redraw(self.area)

    def set_maximized(self, value):
        if value != self.maximized:
            self.maximized = value
            self.area.queue_draw()

    def _set_hover(self, _w, _ev, value):
        self._hover = value
        self.area.queue_draw()
        return False

    def _color(self):
        pal = mn_theme.palette()
        ctx = self.get_style_context()
        if ctx.has_class('destructive-action') or ctx.has_class('mn-close'):
            name = 'onErr' if self._hover else ('err' if ctx.has_class('destructive-action') else 'text')
        elif ctx.has_class('suggested-action'):
            name = 'onPrimary'
        else:
            name = 'text'
        rgba = _rgba(pal[name])
        if not self.is_sensitive():
            rgba = rgba[:3] + (0.45,)
        return rgba

    def _on_draw(self, area, cr):
        alloc = area.get_allocation()
        s = min(alloc.width, alloc.height)
        scale = s / 16.0
        cr.translate((alloc.width - s) / 2.0, (alloc.height - s) / 2.0)
        cr.scale(scale, scale)
        draw_glyph(cr, self.glyph, self._color(), self.maximized)
        return False
