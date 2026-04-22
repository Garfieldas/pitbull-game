import pygame


class UpgradeShop:
    """Render and process an in-game upgrade shop overlay."""

    def __init__(self) -> None:
        self._title_font = pygame.font.SysFont("arial", 42, bold=True)
        self._body_font = pygame.font.SysFont("arial", 24, bold=True)
        self._small_font = pygame.font.SysFont("arial", 18)
        self._upgrades = {
            "insulation": {
                "title": "Stress Insulation",
                "description": "Lower heart attack gain per click.",
                "base_cost": 25,
                "cost_scale": 1.65,
                "max_level": 5,
            },
            "cardio": {
                "title": "Cardio Routine",
                "description": "Slowly recover over time.",
                "base_cost": 35,
                "cost_scale": 1.7,
                "max_level": 5,
            },
            "coupon": {
                "title": "Hydration Habit",
                "description": "Gain extra money per can click.",
                "base_cost": 40,
                "cost_scale": 1.9,
                "max_level": 4,
            },
        }

    def get_cost(self, key: str, level: int) -> int:
        data = self._upgrades[key]
        return int(data["base_cost"] * (data["cost_scale"] ** level))

    def try_buy(self, key: str, money: int, levels: dict[str, int]) -> tuple[int, bool]:
        data = self._upgrades[key]
        level = levels[key]
        if level >= data["max_level"]:
            return money, False

        cost = self.get_cost(key, level)
        if money < cost:
            return money, False

        levels[key] += 1
        return money - cost, True

    def draw(self, screen: pygame.Surface, money: int, levels: dict[str, int]) -> tuple[pygame.Rect, dict[str, pygame.Rect]]:
        width, height = screen.get_size()

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((10, 14, 22, 210))
        screen.blit(overlay, (0, 0))

        panel_w = min(920, width - 40)
        panel_h = min(560, height - 40)
        panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
        panel_rect.center = (width // 2, height // 2)

        pygame.draw.rect(screen, (233, 240, 246), panel_rect, border_radius=16)
        pygame.draw.rect(screen, (25, 35, 50), panel_rect, width=3, border_radius=16)

        title = self._title_font.render("Upgrade Shop", True, (20, 28, 44))
        money_label = self._body_font.render(f"Money: ${money}", True, (25, 80, 40))
        screen.blit(title, title.get_rect(midtop=(panel_rect.centerx, panel_rect.top + 20)))
        screen.blit(money_label, money_label.get_rect(midtop=(panel_rect.centerx, panel_rect.top + 72)))

        close_rect = pygame.Rect(0, 0, 120, 44)
        close_rect.topright = (panel_rect.right - 18, panel_rect.top + 16)
        mouse = pygame.mouse.get_pos()
        close_hover = close_rect.collidepoint(mouse)
        close_color = (190, 70, 70) if close_hover else (155, 58, 58)
        pygame.draw.rect(screen, close_color, close_rect, border_radius=10)
        close_text = self._small_font.render("Close [S]", True, (250, 240, 240))
        screen.blit(close_text, close_text.get_rect(center=close_rect.center))

        cards_top = panel_rect.top + 132
        cards_padding = 18
        card_h = panel_rect.height - 160
        card_w = (panel_rect.width - cards_padding * 4) // 3

        buttons: dict[str, pygame.Rect] = {}
        for idx, key in enumerate(self._upgrades.keys()):
            data = self._upgrades[key]
            level = levels[key]
            cost = self.get_cost(key, level)

            card_rect = pygame.Rect(
                panel_rect.left + cards_padding + idx * (card_w + cards_padding),
                cards_top,
                card_w,
                card_h,
            )

            pygame.draw.rect(screen, (248, 251, 255), card_rect, border_radius=12)
            pygame.draw.rect(screen, (90, 120, 150), card_rect, width=2, border_radius=12)

            title_text = self._body_font.render(data["title"], True, (22, 34, 48))
            desc_text = self._small_font.render(data["description"], True, (64, 72, 88))
            level_text = self._small_font.render(
                f"Level: {level}/{data['max_level']}",
                True,
                (30, 45, 60),
            )
            screen.blit(title_text, title_text.get_rect(midtop=(card_rect.centerx, card_rect.top + 18)))
            screen.blit(desc_text, desc_text.get_rect(midtop=(card_rect.centerx, card_rect.top + 58)))
            screen.blit(level_text, level_text.get_rect(midtop=(card_rect.centerx, card_rect.top + 88)))

            buy_rect = pygame.Rect(0, 0, card_rect.width - 40, 48)
            buy_rect.midbottom = (card_rect.centerx, card_rect.bottom - 24)
            buy_enabled = level < data["max_level"] and money >= cost
            buy_hover = buy_rect.collidepoint(mouse)

            if level >= data["max_level"]:
                btn_text_value = "MAXED"
                btn_color = (118, 126, 134)
            else:
                btn_text_value = f"Buy: ${cost}"
                if buy_enabled:
                    btn_color = (58, 138, 84) if buy_hover else (50, 118, 72)
                else:
                    btn_color = (138, 96, 48)

            pygame.draw.rect(screen, btn_color, buy_rect, border_radius=10)
            btn_text = self._body_font.render(btn_text_value, True, (244, 245, 246))
            screen.blit(btn_text, btn_text.get_rect(center=buy_rect.center))

            buttons[key] = buy_rect

        tip = self._small_font.render("Click upgrade buttons to buy. Press S to open/close.", True, (50, 64, 84))
        screen.blit(tip, tip.get_rect(midbottom=(panel_rect.centerx, panel_rect.bottom - 10)))

        return close_rect, buttons
