import pygame
import os
from Player import Player
from Level import Level

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Game(object):
    def __init__(self):

        # Level setup
        self.currentLevelNumber = 0
        self.levels = []
        self.levels.append(Level(fileName = "levels/level_data/test1.tmx"))
        self.currentLevel = self.levels[self.currentLevelNumber]

        self.overlay = pygame.image.load(os.path.join('images', 'back.png'))
        self.overlay = pygame.transform.scale(self.overlay, (SCREEN_WIDTH, SCREEN_HEIGHT*2))
        self.player = Player()
        self.player.rect.x = 40
        self.player.rect.y = 500 - self.player.image.get_height()
        self.player.currentLevel = self.levels[self.currentLevelNumber]
        self.currentLevel.shiftLevel(0,-9000)
    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            # Keyboard input
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.goLeft()
                elif event.key == pygame.K_RIGHT:
                    self.player.goRight()
                elif event.key == pygame.K_UP:
                    self.player.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.changeX < 0:
                    self.player.stop()
                elif event.key == pygame.K_RIGHT and self.player.changeX > 0:
                    self.player.stop()

    def runLogic(self):
        self.player.update()
        return None

    def draw(self, screen):
        screen.blit(self.overlay, [0,0])
        self.currentLevel.draw(screen)
        self.player.draw(screen)
        pygame.display.flip()
def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    #screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("Pygame Tiled Demo")
    clock = pygame.time.Clock()
    done = False
    game = Game()

    while not done:
        done = game.processEvents()
        game.runLogic()
        game.draw(screen)
        clock.tick(60)

    pygame.quit()


main()