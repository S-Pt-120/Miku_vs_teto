import pygame
from pygame.sprite import Sprite

from paths import resource_path

class Bullet(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

       #load the image
        self.image = pygame.image.load(resource_path("images/bullet.png"))
        self.image = pygame.transform.scale(self.image,(17.8,81.3))
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = float(self.y)

    def draw_bullet(self):
        self.screen.blit(self.image,self.rect)
