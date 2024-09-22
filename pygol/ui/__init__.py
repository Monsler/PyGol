import multiprocessing.process
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import os
from pygol.drawable import Drawable
import threading
import sys

def check_clicks(pos, phase, canvas, event):
    for elem in canvas.drawments:
        elem.clicked(canvas=canvas.pygame_window, phase=phase, pos=pos, event=event)
        

class Window:
    def __init__(self, title: str='PyGol Window', width: int=500, height: int=400) -> None:
        self.title = title
        self.bg = (255, 255, 255)
        self.width = width
        self.height = height
        self.pygame_window = None
        self.window_dispatcher = None
        self.icon = 'logo.png'
        self.drawments = []
        self.is_running = True
        self.window_process = None
        sys.tracebacklimit = 0
    
    def insert(self, of: Drawable):
        self.drawments.append(of)
        of.parent = self
    
    def set_layer(self, of: Drawable, number: int):
        self.drawments.remove(of)
        self.drawments = self.drawments[:number] + [of] + self.drawments[number:-1]

    def _internal_main(self):
        pygame.init()
        self.pygame_window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.DOUBLEBUF)
        pygame.display.set_icon(pygame.image.load(f'{os.path.dirname(__file__)}/logo.png'))
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
        pygame.display.set_caption(self.title)
        clock = pygame.time.Clock()
        while self.is_running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    sys.exit(0)
                    #Finish the window
                elif event.type == pygame.MOUSEBUTTONDOWN:
                   threading.Thread(target=check_clicks, args=(event.pos, 'began', self, event)).start()
                elif event.type == pygame.MOUSEBUTTONUP:
                   threading.Thread(target=check_clicks, args=(event.pos, 'ended', self, event)).start()
                else:
                    if self.window_dispatcher is not None: self.window_dispatcher()

            pygame.display.update()
            self.pygame_window.fill(self.bg)
            for elem in self.drawments:
                elem.on_draw(canvas=self.pygame_window)
                
        
        pygame.quit()
        

    def show(self):
        self.window_process = threading.Thread(target=self._internal_main)
        self.window_process.start()
    
    def exit(self):
        sys.exit(0)