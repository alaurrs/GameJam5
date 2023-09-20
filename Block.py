import pygame
import os


class Block(pygame.sprite.Sprite):
    """
    Spawn a Block
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join('images', 'block.png')).convert()
            img = pygame.transform.scale(img, (50, 50))
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()
