class Settings:

    def __init__(self):

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.bullet_width = 100
        self.bullet_height = 3
        self.bullet_color = (255, 69, 0)
        self.bullets_allowed = 3
        self.ship_image_location = 'images/ship.bmp'
        self.alien_image_location = 'images/alien.bmp'
        self.star_image_location = 'images/bluestar.bmp'
        self.fleet_drop_speed = 10
        self.ship_limit = 3

    def init_dynamic_settings(self, difficulty):
        if difficulty == 'normal':
            self.speedup_scale = 1.1
            self.alien_speed = 1.0
        elif difficulty == 'easy':
            self.speedup_scale = 0.9
            self.alien_speed = 0.5
        elif difficulty == 'hard':
            self.speedup_scale = 1.5
            self.alien_speed = 1.5

        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale



