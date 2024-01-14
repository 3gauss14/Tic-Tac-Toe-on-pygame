import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.win_sound = pygame.mixer.Sound("data/win_sound.mp3")
        self.win_sound.set_volume(0.2)
        self.lose_sound = pygame.mixer.Sound("data/lose_sound.mp3")
        self.lose_sound.set_volume(0.2)

    def play_win_sound(self):
        self.win_sound.play()

    def stop_win_sound(self):
        self.win_sound.stop()

    def play_lose_sound(self):
        self.lose_sound.play()

    def stop_lose_sound(self):
        self.lose_sound.stop()
