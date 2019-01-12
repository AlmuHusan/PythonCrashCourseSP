import sys

import pygame
from settings import Settings
from Ship import ship
from alien import Alien
from pygame.sprite import Group
from game_stats import GameStats
from button import Button

import button
import Ship
import alien
import bullet
import game_functions
import game_stats
import settings

from pygame.sprite import Group
from game_stats import GameStats
from button import Button

import game_functions as gf

def run_game():
       # Initialize game and create a screen object.
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    Shiper= ship(settings,screen)
    alien=Alien(settings,screen)
    bullets = Group()
    aliens = Group()
    stats=GameStats(settings)
    gf.create_fleet(settings,screen,aliens)
    play_button=Button(settings,screen,"Play")
    while True:
        gf.check_events(settings,screen,stats,play_button,Shiper,aliens,bullets)
        if stats.game_active:
            Shiper.update()
            gf.update_bullets(settings,screen,ship,aliens,bullets,stats)
            gf.update_alien(settings,stats,screen,Shiper,aliens,bullets)
        else:
            pygame.display.set_caption("Game Over")


        gf.update_screen(settings,screen,Shiper,aliens,bullets,stats,play_button)
           # Make the most recently drawn screen visible.



run_game()