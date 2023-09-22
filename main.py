import pygame, sys
import os
from Player import Player
from Level import Level
from soundManager import SoundManager
from button import Button


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
START_POS = (-40,600)

sound_manager = SoundManager() 

def get_font(size):
    return pygame.font.Font("images/menu/Juniory.ttf", size)

class Game(object):
    def __init__(self, volume, level):

        # Level setup
        #self.running = True
        self.currentLevelNumber = level
        self.levels = []
        self.levels.append(Level(fileName = "levels/level_data/THE_ARTIST_TILE.tmx"))
        self.levels.append(Level(fileName = "levels/level_data/bwmap1.tmx"))
        self.currentLevel = self.levels[self.currentLevelNumber]

        self.overlay = pygame.image.load(os.path.join('images', 'back.png'))
        self.overlay = pygame.transform.scale(self.overlay, (SCREEN_WIDTH, SCREEN_HEIGHT*2))
        self.player = Player()
        self.player.rect.x = START_POS[0]
        self.player.rect.y = START_POS[1] - self.player.image.get_height()
        self.player.currentLevel = self.levels[self.currentLevelNumber]
        self.currentLevel.shiftLevel(-500,-900)
        self.volume = volume

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
                elif event.key == pygame.K_q:
                    pygame.quit()
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
            OPTIONS_BACK = Button(image=None, pos=(500, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
            
            NEXT_LEVEL = Button(image=None, pos=(980, 460),
                              text_input="Next Level", font=get_font(75), base_color="Black", hovering_color="Green")
            
            while True:
                OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
                OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
                NEXT_LEVEL.changeColor(OPTIONS_MOUSE_POS)
                OPTIONS_BACK.update(screen)
                NEXT_LEVEL.update(screen)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                            print("Back Clicked")
                            self.running = False
                            return 1
                        if NEXT_LEVEL.checkForInput(OPTIONS_MOUSE_POS):
                            print(self.levels)
                            if self.currentLevelNumber < len(self.levels) - 1:
                                print("Next Level -------")
                                self.currentLevelNumber += 1
                                self.currentLevel = self.levels[self.currentLevelNumber]
                                self.player.gameVictory = False
                                pygame.quit()
                                main(self.volume, self.currentLevelNumber)
                            else:
                                print("No more levels available")
                            return 
                        

    def draw(self, screen):
        screen.blit(self.overlay, [0,0])
        self.currentLevel.draw(screen)
        self.player.draw(screen)
        if (self.checkGameLost(screen) == 1):
            return 1
        if (self.checkGameVictory(screen) == 1):
            return 1
        pygame.display.flip()

    def put_block(self,x,y):
        self.player.put_block()
        self.currentLevel.put_block(x, y)

def main(volume, level):
    print("level : " + str(level))
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    #screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    sound_manager.set_volume(volume)
    sound_manager.play_game_music()
    

    pygame.display.set_caption("The Artist")
    clock = pygame.time.Clock()
    done = False
    game = Game(volume, level)
    game.currentLevelNumber = level

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