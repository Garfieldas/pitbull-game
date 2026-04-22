import pygame


class ClickPopup:
    """A short-lived floating text popup for click feedback."""

    def __init__(self, text: str, x: int, y: int, lifetime: float = 0.45) -> None:
        self.text = text
        self.x = float(x)
        self.y = float(y)
        self.lifetime = lifetime
        self.remaining = lifetime
        self.velocity_y = -100.0
        self.font = pygame.font.SysFont("arial", 28, bold=True)

    def update(self, dt: float) -> bool:
        """Advance animation. Returns True while still alive."""
        self.remaining = max(0.0, self.remaining - dt)
        self.y += self.velocity_y * dt
        return self.remaining > 0.0

    def draw(self, screen: pygame.Surface) -> None:
        if self.remaining <= 0.0:
            return

        progress = self.remaining / self.lifetime
        alpha = int(255 * progress)
        text_surface = self.font.render(self.text, True, (190, 32, 32))
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text_surface, text_rect)
