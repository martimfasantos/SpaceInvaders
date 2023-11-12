import pygame
import os
import random
import math
from typing import List
from player import Player
from enemy import Enemy
from constants import FPS, WINDOW, WIDTH, HEIGHT
from constants import RED, GREEN, BLUE
from constants import BG

def main():
    run = True
    clock = pygame.time.Clock()

    # Game settings
    level = 0
    lives = 5
    player_mov = 5
    enemy_mov = 2
    laser_mov = 4
    main_font = pygame.font.SysFont("arial", 25)
    lost_font = pygame.font.SysFont("arial", 100)

    player_ship = Player(WIDTH/2 - 25, HEIGHT - 100)
    lost = False
    lost_count = 0

    enemies_alive: List[Enemy] = []
    enemies_dead: List[Enemy] = []
    wave_lenth = 3
    
    def redraw_window():
        # Top left corner is (0,0)
        WINDOW.blit(pygame.transform.scale(BG, (WIDTH, HEIGHT)) , (0,0))

        # Draw text (lives, health and level)
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - lives_label.get_width() - 35, 10))

        # Draw enemy ships and their lasers
        for enemy_ship in enemies_alive:
            enemy_ship.draw(WINDOW)
            
        # Draw dead enemy lasers 
        for enemy_ship in enemies_dead:
            enemy_ship.draw(WINDOW, alive=False)

        # Draw player and its lasers
        player_ship.draw(WINDOW)

        if lost:
            if not player_ship.is_alive():
                player_ship.explode()
            lost_label = lost_font.render(f"YOU LOST!", 1, (255,255,255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))

        pygame.display.update()

    print('\n--------------------------------------------------------------------')
    print('\tWelcome to \033[1m' + 'SpaceInvaders' + '\033[0m' + '\t\t by martimfasantos')
    print('--------------------------------------------------------------------\n')

    while run:
        clock.tick(FPS)

        if lives < 1 or player_ship.health <= 0:
            lost = True

        if lost:
            lost_count += 1
            if lost_count > FPS * 5:
                run = False

        # Spawn Enemies if last wave was completed
        if not enemies_alive and not lost:
            level += 1
            wave_lenth += 1

            for _ in range(wave_lenth):
                enemy_ship = Enemy(random.randrange(50, WIDTH-100), random.randrange(-HEIGHT, 0), random.choice([RED, GREEN, BLUE]))
                enemies_alive.append(enemy_ship)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if player_ship.is_alive():
            # get all pressed keys
            keys = pygame.key.get_pressed()
            # get all pressed movement keys
            mov_keys = [keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s]]
            num_keys_pressed = sum(mov_keys)
            
            # if more than one key is pressed, normalize movement
            if num_keys_pressed > 1:
                # if up and down are pressed, they cancel each other out
                if keys[pygame.K_w] and keys[pygame.K_s]:
                    mov_keys[2] = False
                    mov_keys[3] = False
                # if left and right are pressed, they cancel each other out
                if keys[pygame.K_a] and keys[pygame.K_d]:
                    mov_keys[0] = False
                    mov_keys[1] = False
            
            norm_mov = math.sqrt(mov_keys.count(True)*(player_mov**2)) / mov_keys.count(True) if mov_keys.count(True) > 0 else 0         
            
            if keys[pygame.K_a]:        # move left
                player_ship.move_left(norm_mov)
            if keys[pygame.K_d]:        # move right
                player_ship.move_right(norm_mov)
            if keys[pygame.K_w]:        # move up
                player_ship.move_up(norm_mov)
            if keys[pygame.K_s]:        # move down
                player_ship.move_down(norm_mov)
            if keys[pygame.K_SPACE]:    # shoot
                player_ship.shoot()

        # Move enemies that are alive and their lasers
        for enemy_ship in enemies_alive[:]:
            enemy_ship.move_down(enemy_mov)
            enemy_ship.move_lasers(laser_mov, player_ship)

            if random.randrange(0, max(6*(FPS - level), 100)) == 1:
                enemy_ship.shoot()

            # when enemy reaches the bottom of the screen
            if enemy_ship.y + enemy_ship.get_height() > HEIGHT:
                if lives > 0:
                    lives -= 1
                enemies_alive.remove(enemy_ship)

            # when player and enemy collide
            if player_ship.collide(enemy_ship):
                player_ship.health -= 10
                enemies_alive.remove(enemy_ship)
                enemies_dead.append(enemy_ship)
                
        # Move lasers of the dead enemies
        for enemy_ship in enemies_dead[:]:
            # Move dead enemy lasers
            if enemy_ship.has_lasers():
                enemy_ship.move_lasers(laser_mov, player_ship)
            # when dead enemy has no more lasers
            else:
                enemies_dead.remove(enemy_ship)

        # Move player lasers
        player_ship.move_lasers(laser_mov, enemies_alive, enemies_dead)        

        redraw_window()

if __name__ == '__main__':
    main()
            