import sys
import pygame
import pygame.font
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            check_keyup(event,ship)
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, ai_settings, screen, ship, bullets,aliens,stats)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(stats,play_button,mouse_x,mouse_y)

def reset_game(ai_settings,screen,aliens,bullets,stats,ship):
    bullets.empty()
    aliens.empty()
    stats.reset_stats()
    ship.center_ship()
    create_fleet(ai_settings,screen,aliens)
    stats.GameOver=False
    stats.game_active=True
    sleep(0.5)

def check_play_button(stats,play_button,mouse_x,mouse_y):
    if play_button.rect.collidepoint(mouse_x,mouse_y):
        stats.game_active=True

def fire_bullet(bullets,ai_settings,screen,ship):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
    if stats.ships_left>0:
        stats.ships_left-=1
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.GameOver=True

def create_fleet(ai_settings,screen,aliens):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    for alien_number in range(number_aliens_x):
        alien = Alien(ai_settings, screen)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        aliens.add(alien)

def check_fleet_x_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_x_edges():
            change_fleet_x_directional(ai_settings,aliens)
            break

def check_fleet_y_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_y_edges():
            change_fleet_y_directional(ai_settings,aliens)
            break

def change_fleet_x_directional(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.fleet_x_direction*=-1

def change_fleet_y_directional(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.fleet_y_direction*=-1

def update_alien(ai_settings,stats,screen,ship,aliens,bullets):
    check_fleet_x_edges(ai_settings,aliens)
    check_fleet_y_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)

def update_screen(settings,screen,ship,aliens,bullets,stats,play_button):
    screen.fill(settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    if stats.game_active==False:
        play_button.draw_button()
    elif stats.GameOver:
        gameover = pygame.image.load('images/gameover.png')
        screen.blit(gameover, gameover.get_rect())
        font = pygame.font.SysFont(None, 48)
        font_text= "Your Score: "+ str(stats.score)
        font_face = font.render(font_text, False, (255, 255, 0))
        font_face_rect=  font_face.get_rect()
        font_face_rect.center = screen.get_rect().center
        screen.blit(font_face,font_face_rect)
    pygame.display.flip()


def update_bullets(ai_settings,screen,ship,aliens,bullets,stats):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets,stats)

def check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets,stats):
    collisions= pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions and not stats.GameOver:
        stats.score+=1
        print(stats.score)
    if len(aliens)==0:
        bullets.empty()
        create_fleet(ai_settings,screen,aliens)

def check_keydown(event,ai_settings,screen,ship,bullets,aliens,stats):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets,ai_settings,screen,ship)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_t:
        if stats.GameOver:
            reset_game(ai_settings,screen,aliens,bullets,stats,ship)

def check_keyup(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False