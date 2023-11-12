import pygame
pygame.font.init()

FPS = 60
WIDTH, HEIGHT = 900, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SpaceInvaders by martimfasantos')

# Colors
YELLOW = 0
RED = 1
GREEN = 2
BLUE = 3

# Spacheships
RED_SPACESHIP = pygame.image.load("./assets/pixel_ship_red.png")
GREEN_SPACESHIP = pygame.image.load("./assets/pixel_ship_green.png")
BLUE_SPACESHIP = pygame.image.load("./assets/pixel_ship_blue.png")

# Player's spaceship
YELLOW_SPACESHIP = pygame.image.load("./assets/pixel_ship_yellow.png")

# Lasers
RED_LASER = pygame.image.load("./assets/pixel_laser_red.png")
GREEN_LASER = pygame.image.load("./assets/pixel_laser_green.png")
BLUE_LASER = pygame.image.load("./assets/pixel_laser_blue.png")
YELLOW_LASER = pygame.image.load("./assets/pixel_laser_yellow.png")

# Cooldowns
LASER_COOLDOWN = FPS / 6

# Effects
EXPLOSION = pygame.image.load("./assets/explosion.png")

# Background
BG = pygame.image.load("./assets/background-black.png")

