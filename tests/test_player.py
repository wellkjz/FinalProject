import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pygame
pygame.init()

from entities.player import Player
from settings import JUMP_FORCE, INVINCIBILITY_FRAMES


def test_initial_lives():
    p = Player(100, 100)
    assert p.lives == 3


def test_take_hit_reduces_lives():
    p = Player(100, 100)
    p.take_hit()
    assert p.lives == 2


def test_invincible_after_hit():
    p = Player(100, 100)
    p.take_hit()
    assert p.is_invincible


def test_dead_after_three_hits():
    p = Player(100, 100)
    p.take_hit(); p.take_hit(); p.take_hit()
    assert not p.is_alive


def test_jump_sets_velocity():
    p = Player(100, 100)
    p.jump()
    assert p.vel_y == JUMP_FORCE