import sys
from time import sleep

import pygame

from game_stats import GameStats
from alien import Alien
from bullet import Bullet
from settings import Settings
from scoreboard import Scoreboard
from ship import Ship
from button import Button

class Alien_invasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_width()
        self.settings.screen_height = self.screen.get_height()
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.create_fleet()
        self.game_active = False
        # 这个开关必须先初始化，否则外星人剩不到 5 个时读它就会 AttributeError
        self.spawning = False
        self.play_button = Button(self, 'play')

    def check_play_button(self,mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.stats.reset_stats()
            # 重置速度和分值要在统计清零之后、重画分数之前做
            self.settings.initialize_dynamic_settings()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.sb.prep_high_score()
            self.game_active = True
            self.spawning = False

            self.bullets.empty()
            self.aliens.empty()

            self.create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_alien_bottom(self):
        for alien in self.aliens.sprites():
            # 用 bottom，中间被判定为“到底”会白白扣命
            if alien.rect.bottom >= self.settings.screen_height:
                self.ship_hit()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def create_aliens(self,x_position,y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def update_aliens(self):
        self.check_fleet_edges()
        self.aliens.update()

        self.check_alien_bottom()

    def create_fleet(self):
        alien = Alien(self)
        alien_width , alien_height = alien.rect.size
        current_x = alien_width
        current_y = alien_height

        while current_y < (self.settings.screen_height - alien_height * 6)  :
            while current_x < (self.settings.screen_width - 1.5 * alien_width):
                self.create_aliens(current_x,current_y)
                current_x += 1.25 * alien_width

            current_x = alien_width
            current_y += 1.5 * alien_height

    def fire_bullets(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def update_bullets(self):
        self.bullets.update()
        # 飞出屏幕顶部的子弹要删掉，否则内存里越积越多
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def check_bullet_aliens_collision(self):
        # 碰撞检测只在主循环里调一次，否则两次 groupcollide 会把外星人提前删掉，
        # 第二次永远检测不到命中，计分和最高分都不会更新
        collisions_1 = pygame.sprite.groupcollide(self.aliens, self.bullets, True, True)
        if collisions_1:
            for aliens in collisions_1.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if len(self.aliens) < 5 and not self.spawning:
            self.spawning = True
            self.create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()
            self.check_alien_bottom()
            # 舰队生成完，解锁（防止连续生成）
        if len(self.aliens) >= 5:
            self.spawning = False

    def ship_hit(self):
        if self.stats.ships_left > 0:
           self.stats.ships_left -= 1
           self.sb.prep_ships()

           self.bullets.empty()
           self.aliens.empty()

           self.create_fleet()
           self.ship.center_ship()

           sleep(1)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def check_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.ship.moving_left = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.ship.moving_right = True
                if event.key == pygame.K_SPACE:
                    self.fire_bullets()
                if event.key == pygame.K_q:
                    sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.ship.moving_left = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.ship.moving_right = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def update_screen(self):
        self.screen.fill(self.settings.bg_colour)
        self.ship.blitme()
        self.sb.show_score()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien in self.aliens.sprites():
            alien.draw_alien()

        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def run_game(self):
        while True:
            self.check_events()
            self.ship.move()

            if self.game_active:
                self.update_bullets()
                self.check_bullet_aliens_collision()
                self.update_aliens()

            self.update_screen()
            self.clock.tick(60)

if __name__ == "__main__":
    ai = Alien_invasion()
    ai.run_game()
