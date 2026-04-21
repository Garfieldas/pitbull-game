import pygame


_FONT = None


def _get_font(size=18):
    global _FONT
    if _FONT is None:
        _FONT = pygame.font.SysFont("arial", size, bold=True)
    return _FONT


def _blend_color(low_color, high_color, t):
    t = max(0.0, min(1.0, t))
    return (
        int(low_color[0] + (high_color[0] - low_color[0]) * t),
        int(low_color[1] + (high_color[1] - low_color[1]) * t),
        int(low_color[2] + (high_color[2] - low_color[2]) * t),
    )


def create_heart_attack_bar_surface(width=420, height=56, level=0.35):
    """Create a top HUD health bar surface from 0.0 to 1.0."""
    level = max(0.0, min(1.0, level))
    width = max(360, int(width))
    height = max(52, int(height))
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    font = _get_font(18)
    label = font.render("HEART ATTACK", True, (25, 25, 30))
    value = font.render(f"{int(level * 100)}%", True, (25, 25, 30))

    outer_rect = pygame.Rect(0, 0, width, height)
    inner_rect = pygame.Rect(6, 6, width - 12, height - 12)
    horizontal_padding = 14
    text_gap = 14
    label_x = inner_rect.x + horizontal_padding
    value_x = inner_rect.right - horizontal_padding - value.get_width()
    meter_x = label_x + label.get_width() + text_gap
    meter_right = value_x - text_gap
    meter_width = max(80, meter_right - meter_x)

    pygame.draw.rect(surface, (32, 32, 36, 220), outer_rect, border_radius=12)
    pygame.draw.rect(surface, (230, 235, 240, 220), inner_rect, border_radius=10)

    meter_rect = pygame.Rect(meter_x, inner_rect.y + 12, meter_width, inner_rect.height - 24)
    pygame.draw.rect(surface, (205, 210, 216), meter_rect, border_radius=8)

    if level > 0:
        fill_width = max(6, int(meter_rect.width * level))
        fill_rect = pygame.Rect(meter_rect.x, meter_rect.y, fill_width, meter_rect.height)
        fill_color = _blend_color((208, 48, 48), (54, 176, 92), level)
        pygame.draw.rect(surface, fill_color, fill_rect, border_radius=8)

    surface.blit(label, (label_x, inner_rect.y + (inner_rect.height - label.get_height()) // 2))
    surface.blit(value, (value_x, inner_rect.y + (inner_rect.height - value.get_height()) // 2))

    return surface
