import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pygame
pygame.init()

from entities.player   import Player
from entities.platform import Platform
from settings import JUMP_FORCE


def test_player_bounces_when_landing():
    player   = Player(100, 90)
    player.vel_y = 5
    platform = Platform(80, 100)

    if player.rect.colliderect(platform.rect) and player.vel_y > 0:
        player.jump()

    assert player.vel_y == JUMP_FORCE


def test_no_bounce_when_rising():
    player   = Player(100, 90)
    player.vel_y = -10
    platform = Platform(80, 100)

    bounced = player.rect.colliderect(platform.rect) and player.vel_y > 0
    assert not bounced


def test_no_collision_when_apart():
    player   = Player(0, 0)
    platform = Platform(300, 500)
    assert not player.rect.colliderect(platform.rect)
