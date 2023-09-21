import pygame
import os
import sys
from Level import Level, SCREEN_HEIGHT, SCREEN_WIDTH
from Layer import Layer

ALPHA = (0, 255, 0)
ani = 4
JUMPCOUNT = 15
WALK_SPEED = 12
MAP_COLLISION_LAYER = 0
MAP_EMPTY_LAYER = 1
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

        self.is_jump = False
        self.jumpCount = JUMPCOUNT
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join('images', 'player_tn.png')).convert()
            img = pygame.transform.scale(img, (125, 125))
            img = img.convert_alpha()  # optimise alpha
            img.set_colorkey(ALPHA)  # set alpha

            imgR = pygame.image.load(os.path.join('images', 'player_run_1_tn.png')).convert()
            imgR = pygame.transform.scale(imgR, (125, 125))
            imgR = imgR.convert_alpha()  # optimise alpha
            imgR.set_colorkey(ALPHA)  # set alpha

            imgR2 = pygame.image.load(os.path.join('images', 'player_run_2_tn.png')).convert()
            imgR2 = pygame.transform.scale(imgR2, (125, 125))
            imgR2 = imgR2.convert_alpha()  # optimise alpha
            imgR2.set_colorkey(ALPHA)  # set alpha

            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()
        self.ground = 720


        self.running = False
        self.runningFrame = 0
        self.runningTime = pygame.time.get_ticks()

        # List of frames for each animation
        self.runningRight = (imgR, img, imgR2)

        self.runningLeft = (pygame.transform.flip(imgR, True, False),
                            pygame.transform.flip(img, True, False),
                            pygame.transform.flip(imgR2, True, False))

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
        self.rect.y -= 20

        if len(tileHitList) > 0:
            self.changeY = -7

    def put_block(self):
        print("FEURjj")


    def update(self):

        self.rect.x += self.changeX

        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)

        tileEmptyList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_EMPTY_LAYER].tiles, False)

        #Move player to correct side of that block
        for tile in tileHitList:
            if self.changeX > 0:
                self.rect.right = tile.rect.left
            else:
                self.rect.left = tile.rect.right

        const = 800
        # Move screen if player reaches screen bounds
        if self.rect.right >= SCREEN_WIDTH - const:
            difference = self.rect.right - (SCREEN_WIDTH - const)
            self.rect.right = SCREEN_WIDTH - const
            self.currentLevel.shiftLevel(-difference, 0)

        # Move screen is player reaches screen bounds
        if self.rect.left <= const:
            difference = const - self.rect.left
            self.rect.left = const
            self.currentLevel.shiftLevel(difference, 0)


        const = 200

        # Move screen if player reaches screen bounds
        if self.rect.bottom >= SCREEN_HEIGHT - const:
            difference = self.rect.bottom - (SCREEN_HEIGHT - const)
            self.rect.bottom = SCREEN_HEIGHT - const
            self.currentLevel.shiftLevel(0, -difference)

        # Move screen is player reaches screen bounds
        if self.rect.top <= const:
            difference = const - self.rect.top
            self.rect.top = const
            self.currentLevel.shiftLevel(0, difference)

        self.rect.y += self.changeY

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

        if len(tileEmptyList) > 0:
            print("Défaite")

        # If player is on ground and running, update running animation
        if self.running and self.changeY == 1:
            if self.direction == "right":
                self.image = self.runningRight[self.runningFrame]
            else:
                self.image = self.runningLeft[self.runningFrame]

        if pygame.time.get_ticks() - self.runningTime > 50:
            self.runningTime = pygame.time.get_ticks()
            if self.runningFrame == 2:
                self.runningFrame = 0
            else:
                self.runningFrame += 1

