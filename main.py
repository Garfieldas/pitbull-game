import pygame
from assets.sprites.redbull_can import RedBullCan
from assets.sprites.heart_attack_bar import create_heart_attack_bar_surface
from assets.sprites.death_screen import draw_death_screen
from assets.sprites.shop_screen import UpgradeShop
from assets.sounds import create_can_click_sound


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
can = RedBullCan()
can_click_sound = create_can_click_sound()
shop = UpgradeShop()
health_level = 0.0
dead = False
shop_open = False
money = 0
upgrade_levels = {"insulation": 0, "cardio": 0, "coupon": 0}
shop_close_rect = None
shop_button_rects = {}
hud_font = pygame.font.SysFont("arial", 24, bold=True)


clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000
    can.update(dt)

    if not dead:
        recovery_per_second = 0.006 + upgrade_levels["cardio"] * 0.015
        health_level = max(0.0, health_level - recovery_per_second * dt)

    can_center = (screen.get_width() // 2, screen.get_height() // 2)
    can_rect = can.get_rect(can_center)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if shop_open:
                shop_open = False
            else:
                running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s and not dead:
            shop_open = not shop_open

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if dead:
                btn_rect = draw_death_screen(screen)
                if btn_rect.collidepoint(event.pos):
                    health_level = 0.0
                    dead = False
                    shop_open = False
            elif shop_open:
                if shop_close_rect is not None and shop_close_rect.collidepoint(event.pos):
                    shop_open = False
                else:
                    for key, button_rect in shop_button_rects.items():
                        if button_rect.collidepoint(event.pos):
                            money, _ = shop.try_buy(key, money, upgrade_levels)
                            break
            elif can.is_clicked(event.pos, can_center):
                can_click_sound.play()
                can.animate()
                money += 1 + upgrade_levels["coupon"]

                click_heart_gain = max(0.01, 0.05 - upgrade_levels["insulation"] * 0.006)
                health_level = min(1.0, health_level + click_heart_gain)
                if health_level >= 1.0:
                    dead = True
                    shop_open = False

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

    screen.fill("white")
    if dead:
        btn_rect = draw_death_screen(screen)
        shop_close_rect = None
        shop_button_rects = {}
    else:
        screen.blit(can.surface, can.get_rect(can_center))
        bar_width = int(min(max(screen.get_width() * 0.56, 320), 780))
        heart_attack_bar_surface = create_heart_attack_bar_surface(width=bar_width, level=health_level)
        bar_rect = heart_attack_bar_surface.get_rect(midtop=(screen.get_width() // 2, 16))
        screen.blit(heart_attack_bar_surface, bar_rect)

        money_text = hud_font.render(f"Money: ${money}", True, (30, 95, 40))
        shop_hint = hud_font.render("S = Shop", True, (40, 40, 55))
        screen.blit(money_text, (16, 18))
        screen.blit(shop_hint, (screen.get_width() - shop_hint.get_width() - 16, 18))

        if shop_open:
            shop_close_rect, shop_button_rects = shop.draw(screen, money, upgrade_levels)
        else:
            shop_close_rect = None
            shop_button_rects = {}

    pygame.display.flip()

pygame.quit()