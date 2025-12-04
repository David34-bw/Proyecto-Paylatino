import pygame
import random
from Constantes import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, img, speed_multiplier, health_bonus):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - ENEMY_WIDTH)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = ENEMY_BASE_SPEED * speed_multiplier
        self.health = ENEMY_BASE_HEALTH + health_bonus

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill() # Remove if it goes off screen without hitting player
