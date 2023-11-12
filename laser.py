import pygame
from constants import HEIGHT

class Laser:
    def __init__(self, x, y, img):
        self.x: float = x
        self.y: float = y
        self.img: pygame.Surface = img
        self.mask: pygame.Surface = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, distance: float):
        self.y -= distance
    
    def off_screen(self):
        return self.y > HEIGHT or self.y < -self.img.get_height()
        
    def collision(self, ship):
        offset_x = ship.x - self.x
        offset_y = ship.y - self.y
        overlap = self.mask.overlap(ship.mask, (offset_x, offset_y))
        return True if overlap and overlap[0] > 0 else False

