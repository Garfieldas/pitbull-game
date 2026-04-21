import math

import pygame


def create_redbull_can_surface(width=180, height=420):
    """Create a simple stylized can image on a transparent surface."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    body_rect = pygame.Rect(20, 20, width - 40, height - 40)
    pygame.draw.ellipse(surface, (180, 190, 210), (20, 0, width - 40, 40))
    pygame.draw.rect(surface, (193, 199, 211), body_rect)
    pygame.draw.ellipse(surface, (170, 180, 198), (20, height - 40, width - 40, 40))

    # Blue and silver split like a Red Bull can.
    half_w = body_rect.width // 2
    pygame.draw.rect(
        surface,
        (25, 65, 150),
        (body_rect.left, body_rect.top + 2, half_w, body_rect.height - 4),
    )
    pygame.draw.rect(
        surface,
        (220, 226, 235),
        (body_rect.left + half_w, body_rect.top + 2, body_rect.width - half_w, body_rect.height - 4),
    )

    # Gold stripe.
    stripe_y = height // 2 - 18
    pygame.draw.rect(surface, (218, 170, 65), (body_rect.left, stripe_y, body_rect.width, 36))

    # Minimal logo hint.
    pygame.draw.circle(surface, (210, 45, 45), (width // 2 - 22, stripe_y + 18), 9)
    pygame.draw.circle(surface, (210, 45, 45), (width // 2 + 22, stripe_y + 18), 9)
    pygame.draw.circle(surface, (235, 198, 90), (width // 2, stripe_y + 18), 8)

    # Top tab.
    pygame.draw.ellipse(surface, (145, 155, 170), (width // 2 - 24, 8, 48, 12))

    return surface


class RedBullCan:
    def __init__(self, width=180, height=420, animation_duration=0.22):
        self.base_surface = create_redbull_can_surface(width=width, height=height)
        self.animation_duration = animation_duration
        self.animation_timer = 0.0
        self.surface = self.base_surface
        self.offset_y = 0

    def update(self, dt):
        self.animation_timer = max(0.0, self.animation_timer - dt)

        if self.animation_timer <= 0:
            self.surface = self.base_surface
            self.offset_y = 0
            return

        progress = 1 - (self.animation_timer / self.animation_duration)
        scale = 1.0 + 0.12 * math.sin(progress * math.pi)
        width = max(1, int(self.base_surface.get_width() * scale))
        height = max(1, int(self.base_surface.get_height() * scale))
        self.offset_y = int(-22 * math.sin(progress * math.pi))
        self.surface = pygame.transform.smoothscale(self.base_surface, (width, height))

    def animate(self):
        self.animation_timer = self.animation_duration

    def get_rect(self, center):
        center_x, center_y = center
        return self.surface.get_rect(center=(center_x, center_y + self.offset_y))

    def is_clicked(self, mouse_pos, center):
        return self.get_rect(center).collidepoint(mouse_pos)
