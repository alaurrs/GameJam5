import pygame.image
import pytmx
import os
from Layer import Layer, Tile, TILESCALE
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
class Level(object):
    def __init__(self, fileName):
        # Create map object from PyTMX
        self.mapObject = pytmx.load_pygame(fileName)

        # Create list of layers for map
        self.layers = []

        # Amount of level shift left/right
        self.levelShift = 0

        # Calculer le décalage pour centrer la tilemap
        map_width = self.mapObject.width * self.mapObject.tilewidth * TILESCALE
        map_height = self.mapObject.height * self.mapObject.tileheight * TILESCALE
        self.levelShiftX = (SCREEN_WIDTH - map_width) // 2
        self.levelShiftY = (SCREEN_HEIGHT - map_height) // 2

        # Create layers for each layer in tile map
        for layer in range(len(self.mapObject.layers)):
            self.layers.append(Layer(index=layer, mapObject=self.mapObject))

    # Move layer left/right
    def shiftLevel(self, shiftX, shiftY):
        self.levelShiftX += shiftX
        self.levelShiftY += shiftY

        for layer in self.layers:
            for tile in layer.tiles:
                tile.rect.x += shiftX
                tile.rect.y += shiftY


    # Update layer
    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)
    def put_block(self,x,y):
        block_img = pygame.image.load(os.path.join("images", "bulle.png"))
        block_img = pygame.transform.scale(block_img, (75,75))
        tile = Tile(block_img, x,y)
        self.layers[0].tiles.add(tile)
