import pygame
import os
import sys

ALPHA = (0, 255, 0)
ani = 4
JUMPCOUNT = 15


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
        self.jumpCount = JUMPCOUNT
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join('images', 'mario.png')).convert()
            img = pygame.transform.scale(img, (100, 100))
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
        if 0 <= (self.rect.x + self.movex) <= 960 - self.image.get_width():
            self.rect.x = self.rect.x + self.movex
        if 0 <= (self.rect.y + self.movey) <= 720 - self.image.get_height():
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
            if self.jumpCount >= -JUMPCOUNT:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.rect.y -= self.jumpCount ** 2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.is_jump = False
                self.rect.y = 720 - self.image.get_height()
                self.jumpCount = JUMPCOUNT
