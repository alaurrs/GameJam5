import pygame, sys
from button import Button
import main
from soundManager import SoundManager

sound_manager = SoundManager() 


def get_font(size, font = 'images/menu/font.ttf'): 
    return pygame.font.Font(font, size)


def main_menu():
    pygame.init()
    volume = 10

    global SCREEN
    SCREEN = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Menu")

    BG = pygame.image.load("images/menu/background.png")
    BG = pygame.transform.scale(BG, (1280, 720))

    # GAME_TITLE = pygame.image.load("images/menu/logo.png")
    # scaled_GAME_TITLE = pygame.transform.scale(GAME_TITLE, (600, 200))

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # TITLE_RECT = scaled_GAME_TITLE.get_rect(center = (640, 100))
        # SCREEN.blit(scaled_GAME_TITLE, TITLE_RECT)

        PLAY_BUTTON = Button(image=pygame.image.load("images/menu/Options Rect.png"), pos=(640, 350), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("images/menu/Options Rect.png"), pos=(640, 500), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/menu/Options Rect.png"), pos=(640, 650), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")


        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    main.main(volume)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    volume = options(volume)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

        

def options(volume):
    input_string = str(volume)
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("Choose Sound volume (1 to 10)", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    # Modifie le volume
                    sound_manager.set_volume(int(input_string) / 10)
                    sound_manager.play_menu_music()
                    return int(input_string)  # return du volume
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # If Backspace is pressed, remove the last character
                    input_string = input_string[:-1]
                elif event.unicode.isdigit():
                    # If a digit is pressed, add it to the input_string
                    new_digit = int(input_string + str(event.unicode))
                    if 1 <= new_digit <= 10:
                        input_string += event.unicode
        text_surface = get_font(45).render(input_string, True, "black")
        text_rect = text_surface.get_rect()
        text_rect.center = (1280 // 2, 720 // 2)
        SCREEN.blit(text_surface, text_rect)

        pygame.display.update()


if __name__ == "__main__":
    sound_manager.play_menu_music()
    main_menu()


