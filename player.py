import pygame
from constants import YELLOW_LASER, YELLOW_SPACESHIP
from constants import EXPLOSION
from constants import WIDTH, HEIGHT
from ship import Ship
from typing import List

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img: pygame.Surface = YELLOW_SPACESHIP
        self.laser_img: pygame.Surface = YELLOW_LASER
        super().setup_ship()

    def move_left(self, distance: float):
        if self.x - distance > 0:
            self.x -= distance

    def move_right(self, distance: float):
        if self.x + distance < WIDTH - self.get_width():
            self.x += distance

    # Top left corner is (0,0)
    def move_up(self, distance: float):
        if self.y - distance > 0:
            self.y -= distance

    # Top left corner is (0,0)
    def move_down(self, distance: float):
        if self.y + distance < HEIGHT - self.get_height():
            self.y += distance
    
    def move_lasers(self, distance: float, enemies_alive: List[Ship], dead_enemies: List[Ship]):
        self.reduce_cooldown()
        for laser in self.lasers:
            laser.move(distance)
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                for enemy in enemies_alive[:]:
                    if laser.collision(enemy):
                        enemies_alive.remove(enemy)
                        dead_enemies.append(enemy)
                        self.lasers.remove(laser)

    def collide(self, ship: Ship):
        offset_x = ship.x - self.x
        offset_y = ship.y - self.y
        overlap = self.mask.overlap(ship.mask, (offset_x, offset_y))
        return True if overlap and overlap[0] > 0 else False
    
    def explode(self):
        self.ship_img = EXPLOSION
        return

    def draw(self, window: pygame.Surface):
        super().draw(window)
        
        if self.is_alive():
            # Health bar
            max_bar_length = 5/6 * self.max_health
            bar_length = self.health/self.max_health * max_bar_length
            pygame.draw.rect(window, (0, 255, 0), (self.x + self.get_width()/2 - max_bar_length/2, self.y + 5/4 * self.get_height(), bar_length, 12))
            pygame.draw.rect(window, (255, 0, 0), (self.x + self.get_width()/2 - max_bar_length/2 + bar_length, self.y + 5/4 * self.get_height(), max_bar_length - bar_length, 12))
            pygame.draw.rect(window, (255, 255, 255), (self.x + self.get_width()/2 - max_bar_length/2, self.y + 5/4 * self.get_height(), max_bar_length, 12), 2)
            