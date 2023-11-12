from constants import LASER_COOLDOWN
from laser import Laser
from typing import List
import pygame

class Ship():
    def __init__(self, x, y, health = 100):
        self.x: float = x
        self.y: float = y
        self.health: int = health
        self.ship_img: pygame.Surface = None
        self.laser_img: pygame.Surface = None
        self.lasers: List[Laser] = []
        self.cooldown: float = 0
        
    def setup_ship(self):
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = self.health

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
    
    def is_alive(self):
        return True if self.health > 0 else False

    def reduce_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def can_shoot(self):
        return True if not self.cooldown else False

    def shoot(self):
        if self.can_shoot():
            self.lasers.append(Laser(self.x, self.y, self.laser_img))
            self.cooldown = LASER_COOLDOWN

    def move_lasers(self, distance: float, obj):
        # implemented in subclasses
        pass
    
    def has_lasers(self):
        return True if len(self.lasers) > 0 else False

    def explode(self):
        # implemented in subclasses
        pass

    def draw(self, window: pygame.Surface, alive=True):
        # Ship
        if alive:
            window.blit(self.ship_img, (self.x, self.y))
        
        # Lasers
        for laser in self.lasers:
            laser.draw(window)
