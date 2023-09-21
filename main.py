import pygame
import os
from Player import Player
from Level import Level
from soundManager import SoundManager

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

sound_manager = SoundManager() 

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
        self.currentLevel.shiftLevel(0,-6600)
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
                elif event.key == pygame.K_j:
                    print("J")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.changeX < 0:
                    self.player.stop()
                elif event.key == pygame.K_RIGHT and self.player.changeX > 0:
                    self.player.stop()
            if pygame.mouse.get_pressed(3)[0] == True:
                mousePos = pygame.mouse.get_pos()
                # Arrondir mousePos[0] et mousePos[1] aux multiples de 24
                rounded_x = round(mousePos[0] / 50) * 50
                rounded_y = round(mousePos[1] / 50) * 50
                self.put_block(rounded_x, rounded_y)
    def runLogic(self):
        self.player.update()
        return None

    def draw(self, screen):
        screen.blit(self.overlay, [0,0])
        self.currentLevel.draw(screen)
        self.player.draw(screen)
        pygame.display.flip()

    def put_block(self,x,y):
        self.player.put_block()
        self.currentLevel.put_block(x, y)

def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    #screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    sound_manager.play_game_music()

    pygame.display.set_caption("The Artist")
    clock = pygame.time.Clock()
    done = False
    game = Game()

    while not done:
        done = game.processEvents()
        game.runLogic()
        game.draw(screen)
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()