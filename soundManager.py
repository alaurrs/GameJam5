import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.menu_music = pygame.mixer.Sound("sfx/menu_sound.wav")
        self.game_music = pygame.mixer.Sound("sfx/happyLevel.wav")
        self.jump_sound = pygame.mixer.Sound("sfx/jump.wav")
        self.current_music = None
        self.volume = 1.0  # Volume par défaut (0.0 à 1.0)
    
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        
        # Appliquez le volume actuel à chaque canal sonore
        self.menu_music.set_volume(self.volume)
        self.game_music.set_volume(self.volume)
        self.jump_sound.set_volume(self.volume)

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


