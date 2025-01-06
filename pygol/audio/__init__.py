import pygame

class Audio:
    def __init__(self, audio_path) -> None:
        pygame.mixer.init()
        self.audio = audio_path
    
    def play(self, loops: int):
        pygame.mixer.music.load(self.audio)
        pygame.mixer.music.play(loops, 0)
    
    def stop(self):
        pygame.mixer.music.stop()