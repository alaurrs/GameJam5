#!/usr/bin/env python3
# by Seth Kenlon

# GPLv3
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from typing import Tuple

import pygame
import sys
import os
from Player import Player
from Block import Block

'''
Variables
'''

worldx = 960
worldy = 720
fps = 60
world = pygame.display.set_mode([worldx, worldy])

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)

'''
Setup
'''

backdrop = pygame.image.load(os.path.join('images', 'stage.png'))
clock = pygame.time.Clock()
pygame.init()
backdropbox = world.get_rect()
main = True

player = Player()  # spawn player
player.rect.x = 0  # go to x
player.rect.y = worldy - player.image.get_width()  # go to y
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 10

'''
Objects
'''
block_list = pygame.sprite.Group()

'''
Main Loop
'''


def update():
    is_collide = collision(player)
    return None


def collision(box1, box2):
    if (((box2.rect.x >= box1.rect.x + box1.w)  # trop à droite
         or (box2.x + box2.w <= box1.x)  # trop à gauche
         or (box2.y >= box1.y + box1.h)  # trop en bas
         or (box2.y + box2.h <= box1.y))):  # trop en haut
        return False
    else:
        return True


def put_block():
    block = Block()
    block.rect.x = player.rect.x + 50
    block.rect.y = player.rect.y
    block_list.add(block)
    block_list.draw(backdrop)
    print(block_list)
    print("block")


while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False

        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps, 0)
            if event.key == pygame.K_j:
                print("j")
                put_block()
            if not player.is_jump:
                if event.key == pygame.K_UP or event.key == ord('w') or event.key == pygame.K_SPACE:
                    print('jump')
                    player.is_jump = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps, 0)

    world.blit(backdrop, backdropbox)
    update()
    player.update()
    player_list.draw(world)
    pygame.display.flip()
    clock.tick(fps)
