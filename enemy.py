import pygame
from ship import Ship
from constants import RED, RED_LASER, RED_SPACESHIP
from constants import GREEN, GREEN_LASER, GREEN_SPACESHIP
from constants import BLUE, BLUE_LASER, BLUE_SPACESHIP

class Enemy(Ship):

    COLOR_MAP = {
        RED : (RED_SPACESHIP, RED_LASER),
        GREEN : (GREEN_SPACESHIP, GREEN_LASER),
        BLUE : (BLUE_SPACESHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img: pygame.Surface = self.COLOR_MAP[color][0]
        self.laser_img: pygame.Surface = self.COLOR_MAP[color][1]
        super().setup_ship()


    # Top left corner is (0,0)
    def move_down(self, distance: float):
        self.y += distance

    def move_lasers(self, distance: float, player_ship: Ship):
        self.reduce_cooldown()
        for laser in self.lasers:
            laser.move(-distance)
            if laser.off_screen():
                self.lasers.remove(laser)
            elif laser.collision(player_ship):
                player_ship.health -= 10
                self.lasers.remove(laser)
