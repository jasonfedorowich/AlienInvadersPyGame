import sys
from random import randint
from time import sleep
import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from high_score import HighScoreManager
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from star import Star
from game_stats import GameStats


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption('Alien Invasion')
        self.hs = HighScoreManager(self.settings.score_file_location)

        self.stats = GameStats(self)
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self._create_stars()
        self.normal_button = Button(self, 'Normal', self.screen.get_rect().center)
        midtop = self.screen.get_rect().midtop
        self.easy_button = Button(self, 'Easy', (midtop[0], midtop[1] + 30))

        midbottom = self.screen.get_rect().midbottom
        self.hard_button = Button(self, 'Hard', (midbottom[0], midbottom[1] - 30))
        self.sb = Scoreboard(self)


    def run_game(self):

        while True:

            self._check_events()

            if self.stats.game_active:
                self.ship.update()

                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.hs.save_high_score(self.stats.high_score)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game('normal')

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.sb.show_score()
        self.stars.draw(self.screen)

        if not self.stats.game_active:
            self.normal_button.draw_button()
            self.easy_button.draw_button()
            self.hard_button.draw_button()

        pygame.display.flip()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            bullet = Bullet(self)
            self.bullets.add(bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_of_rows = available_space_y // (2 * alien_height)
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_of_aliens_x = available_space_x // (2 * alien_width)
        for row_number in range(number_of_rows):
            for alien_number in range(number_of_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_stars(self):
        star = Star(self)
        star_width, star_height = star.rect.size

        available_space_y = self.settings.screen_height
        number_of_rows = available_space_y // star_height
        available_space_x = self.settings.screen_width - (2 * star_width)
        max_number_of_cols = available_space_x // (2 * star_width)

        number_of_stars = randint(0, (max_number_of_cols//2))

        for row_number in range(number_of_rows):
            for star_number in range(number_of_stars):
                self._create_star(row_number, max_number_of_cols)

    def _create_star(self, row_number, max_number):
        star = Star(self)
        star_width, star_height = star.rect.size
        star_number = randint(0, max_number)

        star.x = star_width + 2 * star_width * star_number
        star.rect.x = star.x
        star.rect.y = star.rect.height + 2 * star.rect.height * row_number
        self.stars.add(star)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)

            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
            self.sb.prep_ships()
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _start_game(self, difficulty):
        self.stats.reset_stats()
        self.stats.game_active = True

        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)
        self.settings.init_dynamic_settings(difficulty)

    def _check_play_button(self, mouse_pos):
        if not self.stats.game_active:
            normal_button_clicked = self.normal_button.rect.collidepoint(mouse_pos)
            hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
            easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)

            if normal_button_clicked:
                self._start_game('normal')
            elif hard_button_clicked:
                self._start_game('hard')
            elif easy_button_clicked:
                self._start_game('easy')


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
