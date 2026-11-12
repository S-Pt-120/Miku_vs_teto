import pygame
from pygame.sprite import Sprite

from paths import resource_path

class Ship(Sprite):
    def __init__(self,ai_game,size=(128, 176)):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        #load the image
        self.image = pygame.image.load(resource_path('images/miku.bmp'))
        self.image = pygame.transform.scale(self.image,size)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        #move
        self.moving_right = False
        self.moving_left = False

    def move(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed

    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


