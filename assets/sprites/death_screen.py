import pygame


def draw_death_screen(screen):
    """Draw a full-screen death overlay. Returns True if the player clicks Restart."""
    w, h = screen.get_width(), screen.get_height()

    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((18, 4, 4, 230))
    screen.blit(overlay, (0, 0))

    font_big = pygame.font.SysFont("arial", max(48, h // 12), bold=True)
    font_mid = pygame.font.SysFont("arial", max(26, h // 22), bold=True)
    font_small = pygame.font.SysFont("arial", max(20, h // 30))

    title = font_big.render("YOU HAD A HEART ATTACK", True, (220, 40, 40))
    subtitle = font_mid.render("Too much Cortisol.", True, (210, 180, 180))

    btn_rect = pygame.Rect(0, 0, max(220, w // 5), max(60, h // 12))
    btn_rect.center = (w // 2, h // 2 + max(80, h // 8))
    mouse = pygame.mouse.get_pos()
    btn_hover = btn_rect.collidepoint(mouse)
    btn_color = (200, 50, 50) if btn_hover else (140, 30, 30)
    pygame.draw.rect(screen, btn_color, btn_rect, border_radius=14)
    btn_label = font_small.render("Restart", True, (255, 235, 235))
    screen.blit(btn_label, btn_label.get_rect(center=btn_rect.center))

    screen.blit(title, title.get_rect(center=(w // 2, h // 2 - max(80, h // 9))))
    screen.blit(subtitle, subtitle.get_rect(center=(w // 2, h // 2 - max(20, h // 25))))

    return btn_rect
