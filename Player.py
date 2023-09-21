import pygame
import os
import sys
from Level import Level
from Layer import Layer

ALPHA = (0, 255, 0)
ani = 4
JUMPCOUNT = 15
WALK_SPEED = 12
MAP_COLLISION_LAYER = 0
class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Speed and direction
        self.changeX = 0
        self.changeY = 0
        self.direction = "right"

        self.running = False
        self.runningFrame = 0
        self.is_jump = False
        self.jumpCount = JUMPCOUNT
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join('images', 'mario.png')).convert()
            img = pygame.transform.scale(img, (200, 200))
            img = img.convert_alpha()  # optimise alpha
            img.set_colorkey(ALPHA)  # set alpha
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()
        self.ground = 720

        self.runningTime = pygame.time.get_ticks()

        self.currentLevel = None
    def draw(self,screen):
        screen.blit(self.image, self.rect)

    def goRight(self):
        self.direction = "right"
        self.running = True
        self.changeX = WALK_SPEED

    def goLeft(self):
        self.direction = "left"
        self.running = True
        self.changeX = -WALK_SPEED

    def stop(self):
        self.running = False
        self.changeX = 0

    def jump(self):
        self.rect.y += 5
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 8

        if len(tileHitList) > 0:
            self.changeY = -10

    def update(self):

        self.rect.x += self.changeX

        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)

        if len(tileHitList) > 0 :

            for tile in tileHitList:
                if self.changeY > 0:
                    self.rect.bottom = tile.rect.top
                    self.changeY = 1

                else:
                    self.rect.top = tile.rect.bottom
                    self.changeY = 0
        else:
            self.changeY += 0.2

        if pygame.time.get_ticks() - self.runningTime > 50:
            self.runningTime = pygame.time.get_ticks()
            if self.runningFrame == 4:
                self.runningFrame = 0
            else:
                self.runningFrame += 1


        self.rect.y += self.changeY