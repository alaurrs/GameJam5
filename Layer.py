import pygame

TILESCALE = 0.25

class Layer(object):
    def __init__(self, index, mapObject):
        # Layer index from tiled map
        self.index = index

        # Create gruop of tiles for this layer
        self.tiles = pygame.sprite.Group()

        # Reference map object
        self.mapObject = mapObject

        # Create tiles in the right position for each layer
        for x in range(self.mapObject.width):
            for y in range(self.mapObject.height):
                img = self.mapObject.get_tile_image(x, y, self.index)
                if img:
                    img = pygame.transform.scale(img, ((int(self.mapObject.tilewidth * TILESCALE)), ((int(self.mapObject.tilewidth * TILESCALE)))))
                    self.tiles.add(Tile(image=img, x=(x * self.mapObject.tilewidth*TILESCALE), y=(y * self.mapObject.tileheight*TILESCALE)))

    # Draw layer
    def draw(self, screen):
        self.tiles.draw(screen)


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y