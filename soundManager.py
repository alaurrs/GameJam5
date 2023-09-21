import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.menu_music = pygame.mixer.Sound("sfx/menu_sound.wav")
        self.game_music = pygame.mixer.Sound("sfx/happyLevel.wav")
        self.jump_sound = pygame.mixer.Sound("sfx/jump.wav")
        self.current_music = None

    def play_menu_music(self):
        # Arrête la musique actuelle si elle est en cours de lecture
        if self.current_music:
            self.current_music.stop()
      
        self.menu_music.play(-1)
        self.current_music = self.menu_music

    def play_game_music(self):
        if self.current_music:
            self.current_music.stop()
     
        self.game_music.play(-1)
        self.current_music = self.game_music
    
    def play_jump_sound(self):
        self.jump_sound.play()


    def stop_music(self):
        if self.current_music:
            self.current_music.stop()


