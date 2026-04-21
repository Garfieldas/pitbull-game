import pygame
from assets.sprites.redbull_can import RedBullCan
from assets.sprites.heart_attack_bar import create_heart_attack_bar_surface
from assets.sprites.death_screen import draw_death_screen
from assets.sounds import create_can_click_sound


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
can = RedBullCan()
can_click_sound = create_can_click_sound()
health_level = 0.0
dead = False


clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000
    can.update(dt)
    can_center = (screen.get_width() // 2, screen.get_height() // 2)
    can_rect = can.get_rect(can_center)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if dead:
                btn_rect = draw_death_screen(screen)
                if btn_rect.collidepoint(event.pos):
                    health_level = 0.0
                    dead = False
            elif can.is_clicked(event.pos, can_center):
                can_click_sound.play()
                can.animate()
                health_level = min(1.0, health_level + 0.05)
                if health_level >= 1.0:
                    dead = True

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

    screen.fill("white")
    if dead:
        btn_rect = draw_death_screen(screen)
    else:
        screen.blit(can.surface, can.get_rect(can_center))
        bar_width = int(min(max(screen.get_width() * 0.56, 320), 780))
        heart_attack_bar_surface = create_heart_attack_bar_surface(width=bar_width, level=health_level)
        bar_rect = heart_attack_bar_surface.get_rect(midtop=(screen.get_width() // 2, 16))
        screen.blit(heart_attack_bar_surface, bar_rect)

    pygame.display.flip()

pygame.quit()