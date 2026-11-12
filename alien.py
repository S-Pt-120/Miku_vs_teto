import pygame
from pygame.sprite import Sprite

from paths import resource_path

class Alien(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load(resource_path('images/teto.bmp'))
        # 原图 667x500 太大，先缩小，否则一个就占掉小半个屏幕
        self.image = pygame.transform.scale(self.image, (120, 90))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def draw_alien(self):
        self.screen.blit(self.image,self.rect)


