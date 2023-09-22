import pygame, sys
import os
from Player import Player
from Level import Level
from soundManager import SoundManager
from button import Button


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

sound_manager = SoundManager() 

def get_font(size):
    return pygame.font.Font("images/menu/font.ttf", size)

class Game(object):
    def __init__(self):

        # Level setup
        self.currentLevelNumber = 0
        self.levels = []
        self.levels.append(Level(fileName = "levels/level_data/bwmap1.tmx"))
        self.currentLevel = self.levels[self.currentLevelNumber]

        self.overlay = pygame.image.load(os.path.join('images', 'back.png'))
        self.overlay = pygame.transform.scale(self.overlay, (SCREEN_WIDTH, SCREEN_HEIGHT*2))
        self.player = Player()
        self.player.rect.x = 40
        self.player.rect.y = 500 - self.player.image.get_height()
        self.player.currentLevel = self.levels[self.currentLevelNumber]
        self.currentLevel.shiftLevel(-500,-900)
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
            else:
                self.player.stop()
            if pygame.mouse.get_pressed(3)[0] == True:
                mousePos = pygame.mouse.get_pos()
                # Arrondir mousePos[0] et mousePos[1] aux multiples de 75
                round_player_x = self.player.rect.x
                round_player_y = self.player.rect.y
                rounded_x = round(mousePos[0] / 75) * 75
                rounded_y = round(mousePos[1] / 75) * 75
                if abs(rounded_x - round_player_x) >= 75 or abs(rounded_y - round_player_y) >= 75:
                    self.put_block(rounded_x, rounded_y)
    def runLogic(self):
        if not self.player.gameLost and not self.player.gameVictory:
            self.player.update()
        return None

    def checkGameLost(self, screen):
        if self.player.gameLost:
            DEFEAT_TEXT = get_font(100).render("DEFEAT", True, "#b68f40")
            DEFEAT_RECT = DEFEAT_TEXT.get_rect(center=(640, 100))
            screen.blit(DEFEAT_TEXT, DEFEAT_RECT)
            OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
            while True:
                OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
                OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
                OPTIONS_BACK.update(screen)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                            print("Back Clicked")
                            return 1
        else:
            return 0

    def checkGameVictory(self, screen):
        if self.player.gameVictory:
            VICTORY_TEXT = get_font(100).render("VICTORY", True, "#b68f40")
            VICTORY_RECT = VICTORY_TEXT.get_rect(center=(640, 100))
            screen.blit(VICTORY_TEXT, VICTORY_RECT)
            pygame.display.update()
            return self.player.gameVictory

    def draw(self, screen):
        screen.blit(self.overlay, [0,0])
        self.currentLevel.draw(screen)
        self.player.draw(screen)
        if (self.checkGameLost(screen) == 1):
            return 1
        self.checkGameVictory(screen)
        pygame.display.flip()

    def put_block(self,x,y):
        self.player.put_block()
        self.currentLevel.put_block(x, y)

def main(volume):
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    #screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    sound_manager.set_volume(volume)
    sound_manager.play_game_music()
    

    pygame.display.set_caption("The Artist")
    clock = pygame.time.Clock()
    done = False
    game = Game()

    while not done:
        done = game.processEvents()
        game.runLogic()
        if (game.draw(screen) == 1):
            pygame.quit()
            return 1
        #game.checkGameLost(screen)
        clock.tick(60)


if __name__ == '__main__':
    main()