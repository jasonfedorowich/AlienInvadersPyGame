import pygame
from pygame.sprite import Sprite


class Raindrop(Sprite):
    def __init__(self, raindrop_game):
        super().__init__()
        self.screen = raindrop_game.screen
        self.image = pygame.image.load('raindrop.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.downwards_speed = 1
        self.bg_color = (230, 230, 230)

    def update(self):
        self.y += self.downwards_speed
        self.rect.y = self.y

    def is_at_bottom(self):
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom:
            return True


class Raindrops:
    def __init__(self):
        self.bg_color = (230, 230, 230)
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 800

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        pygame.display.set_caption('Raindrops')

        self.raindrops = pygame.sprite.Group()
        self._create_raindrops()

    def run_game(self):
        while True:
            self._update_raindrops()
            self._update_screen()

    def _update_screen(self):
        self.screen.fill(self.bg_color)

        self.raindrops.draw(self.screen)
        pygame.display.flip()

    def _create_raindrops(self):
        raindrop = Raindrop(self)
        raindrop_width, raindrop_height = raindrop.rect.size

        available_space_y = (self.screen_height - (3 * raindrop_height))
        number_of_rows = available_space_y // (2 * raindrop_height)
        available_space_x = self.screen_width - (2 * raindrop_width)
        number_of_raindrops_x = available_space_x // (2 * raindrop_width)
        for row_number in range(number_of_rows):
            for raindrop_number in range(number_of_raindrops_x):
                self._create_raindrop(raindrop_number, row_number)

    def _create_raindrop(self, alien_number, row_number):
        raindrop = Raindrop(self)
        raindrop_widith, raindrop_height = raindrop.rect.size
        raindrop.x = raindrop_widith + 2 * raindrop_widith * alien_number
        raindrop.rect.x = raindrop.x
        raindrop.rect.y = raindrop.rect.height + 2 * raindrop.rect.height * row_number
        raindrop.y = raindrop.rect.y
        self.raindrops.add(raindrop)

    def _update_raindrops(self):
        self._check_if_row_gone()
        self._update_raindrops_position()

    def _check_if_row_gone(self):
        need_new_row = False
        for raindrop in self.raindrops.sprites().copy():
            if raindrop.is_at_bottom():
                self.raindrops.remove(raindrop)
                need_new_row = True

        print(len(self.raindrops))
        if need_new_row:
            self._create_new_row()

    def _create_new_row(self):

        pass

    def _update_raindrops_position(self):
        for raindrop in self.raindrops:
            raindrop.update()
        pass


if __name__ == '__main__':
    ai = Raindrops()
    ai.run_game()
