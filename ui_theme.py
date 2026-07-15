"""Small, dependency-free UI helpers shared by the Pygame screens."""

import ctypes
import sys
import pygame


BG = (15, 23, 42)
SURFACE = (30, 41, 59)
SURFACE_2 = (51, 65, 85)
TEXT = (241, 245, 249)
MUTED = (148, 163, 184)
ACCENT = (56, 189, 248)
ACCENT_DARK = (14, 116, 144)
SUCCESS = (52, 211, 153)
DANGER = (251, 113, 133)
BORDER = (71, 85, 105)


def _app_icon():
    """Build a crisp, neutral spritesheet icon without an external asset."""
    icon = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.rect(icon, BG, icon.get_rect(), border_radius=7)
    tiles = (
        (pygame.Rect(5, 5, 10, 10), ACCENT),
        (pygame.Rect(17, 5, 10, 10), (34, 211, 238)),
        (pygame.Rect(5, 17, 10, 10), (14, 165, 233)),
        (pygame.Rect(17, 17, 10, 10), (45, 212, 191)),
    )
    for rect, color in tiles:
        pygame.draw.rect(icon, color, rect, border_radius=2)
    pygame.draw.rect(icon, BORDER, icon.get_rect(), 1, border_radius=7)
    return icon


def configure_window():
    """Apply the app icon and a native dark title bar when supported by Windows."""
    pygame.display.set_icon(_app_icon())
    if sys.platform != "win32":
        return

    try:
        hwnd = pygame.display.get_wm_info()["window"]
        dwm = ctypes.windll.dwmapi

        # Native controls remain fully functional while matching the application.
        dark = ctypes.c_int(1)
        result = dwm.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(dark), ctypes.sizeof(dark))
        if result != 0:  # Older Windows 10 builds use attribute 19.
            dwm.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(dark), ctypes.sizeof(dark))

        def colorref(rgb):
            red, green, blue = rgb
            return ctypes.c_int(red | (green << 8) | (blue << 16))

        caption = colorref(SURFACE)
        title_text = colorref(TEXT)
        border = colorref(BORDER)
        dwm.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(caption), ctypes.sizeof(caption))
        dwm.DwmSetWindowAttribute(hwnd, 36, ctypes.byref(title_text), ctypes.sizeof(title_text))
        dwm.DwmSetWindowAttribute(hwnd, 34, ctypes.byref(border), ctypes.sizeof(border))
    except (AttributeError, KeyError, OSError):
        # Icon customization still works on unsupported Windows versions.
        pass


def font(size, bold=False):
    return pygame.font.SysFont("segoeui", size, bold=bold)


def text(surface, value, face, color, pos, center=False):
    image = face.render(str(value), True, color)
    rect = image.get_rect(center=pos) if center else image.get_rect(topleft=pos)
    surface.blit(image, rect)
    return rect


def rounded_panel(surface, rect, color=SURFACE, border=BORDER, radius=16):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, 1, border_radius=radius)


def checkerboard(surface, rect, cell=16):
    colors = ((38, 50, 68), (47, 61, 80))
    pygame.draw.rect(surface, colors[0], rect, border_radius=14)
    for y in range(rect.top, rect.bottom, cell):
        for x in range(rect.left, rect.right, cell):
            color = colors[((x - rect.left) // cell + (y - rect.top) // cell) % 2]
            pygame.draw.rect(surface, color, pygame.Rect(x, y, min(cell, rect.right-x), min(cell, rect.bottom-y)))


def button(surface, rect, label, face, mouse_pos, primary=False, enabled=True, icon=""):
    hovered = enabled and rect.collidepoint(mouse_pos)
    if not enabled:
        fill, fg = (38, 49, 66), (100, 116, 139)
    elif primary:
        fill, fg = ((14, 165, 233) if hovered else ACCENT), BG
    else:
        fill, fg = ((65, 81, 105) if hovered else SURFACE_2), TEXT
    pygame.draw.rect(surface, fill, rect, border_radius=10)
    pygame.draw.rect(surface, ACCENT if hovered else BORDER, rect, 1, border_radius=10)
    text(surface, f"{icon}  {label}" if icon else label, face, fg, rect.center, center=True)


def pill(surface, rect, label, face, active=True):
    fill = (19, 78, 74) if active else (51, 65, 85)
    fg = SUCCESS if active else MUTED
    pygame.draw.rect(surface, fill, rect, border_radius=rect.height // 2)
    text(surface, label, face, fg, rect.center, center=True)


def toggle_button(surface, rect, label, face, small_face, mouse_pos, active, enabled=True):
    """Draw a toggle with separate label and state areas."""
    hovered = enabled and rect.collidepoint(mouse_pos)
    fill = (65, 81, 105) if hovered else SURFACE_2
    fg = TEXT if enabled else (100, 116, 139)
    if not enabled:
        fill = (38, 49, 66)
    pygame.draw.rect(surface, fill, rect, border_radius=10)
    pygame.draw.rect(surface, ACCENT if hovered else BORDER, rect, 1, border_radius=10)
    text(surface, label, face, fg, (rect.x + 14, rect.centery - face.get_height() // 2))
    state_rect = pygame.Rect(rect.right - 50, rect.centery - 9, 40, 18)
    pill(surface, state_rect, "ON" if active else "OFF", small_face, active and enabled)


def stat(surface, x, y, label, value, label_face, value_face):
    text(surface, label.upper(), label_face, MUTED, (x, y))
    text(surface, value, value_face, TEXT, (x, y + 18))
