class Settings:

    def __init__(self):

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5

        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 69, 0)
        self.bullets_allowed = 3
        self.ship_image_location = 'images/ship.bmp'
        self.alien_image_location = 'images/alien.bmp'
        self.star_image_location = 'images/bluestar.bmp'
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
