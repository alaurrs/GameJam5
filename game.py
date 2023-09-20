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

'''
Variables
'''

worldx = 960
worldy = 720
fps = 40
ani = 4
world = pygame.display.set_mode([worldx, worldy])

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

'''
Objects
'''


class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.mass = 1
        self.vel = 5
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.is_jump = False
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join('images', 'mario.png')).convert()
            img = pygame.transform.scale(img, (50, 50))
            img = img.convert_alpha()  # optimise alpha
            img.set_colorkey(ALPHA)  # set alpha
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

    def control(self, x, y):
        """
        control player movement
        """
        self.movex += x
        self.movey += y

    def update(self):
        """
        Update sprite position
        """

        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        # moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = self.images[self.frame // ani]
            
        # jump
        if self.is_jump:
            # calculate force (F). F = 1 / 2 * mass * velocity ^ 2.
            F_orce = (1 / 2) * self.mass * (self.vel ** 2)

            # change in the y co-ordinate
            self.movey -= F_orce

            # decreasing velocity while going up and become negative while coming down
            self.vel = self.vel - 1

            # object reached its maximum height
            if self.vel < 0:
                print("test3")
                # negative sign is added to counter negative velocity
                self.mass = -1
            # objected reaches its original state
            if self.vel == -6:
                print("test")
                # making isjump equal to false
                self.is_jump = False

                # setting original values to v and m
                self.vel = 5
                self.mass = 1


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
player.rect.y = worldy - 50  # go to y
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 10

'''
Main Loop
'''

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
    player.update()
    player_list.draw(world)
    pygame.display.flip()
    clock.tick(fps)
