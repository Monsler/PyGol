import multiprocessing.process
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import os
from pygol.drawable import Drawable
import threading
import sys

VERSION = "2024.09@beta"

def check_clicks(pos, phase, canvas, event):
    for elem in canvas.drawments:
        elem.clicked(canvas=canvas.pygame_window, phase=phase, pos=pos, event=event)
        
class Key:
    a = pygame.K_a
    b = pygame.K_b
    c = pygame.K_c
    d = pygame.K_d
    e = pygame.K_e
    f = pygame.K_f
    g = pygame.K_g
    h = pygame.K_h
    i = pygame.K_a
    j = pygame.K_j
    k = pygame.K_k
    l = pygame.K_l
    m = pygame.K_m
    n = pygame.K_n
    o = pygame.K_o
    p = pygame.K_p
    q = pygame.K_q
    r = pygame.K_r
    s = pygame.K_s
    t = pygame.K_t
    u = pygame.K_u
    v = pygame.K_v
    w = pygame.K_w
    x = pygame.K_x
    y = pygame.K_y
    z = pygame.K_z
    one = pygame.K_1
    two = pygame.K_2
    three = pygame.K_3
    four = pygame.K_4
    five = pygame.K_5
    six = pygame.K_6
    seven = pygame.K_7
    eight = pygame.K_8
    nine = pygame.K_9

class Window:
    def __init__(self, title: str='PyGol Window', width: int=500, height: int=400) -> None:
        print(f'Welcome to PyGol {VERSION}')
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
        self.key_event = None
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
        pygame.display.set_icon(pygame.image.load(f'{self.icon}'))
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
        pygame.display.set_caption(self.title)
        pygame.mixer.init(frequency=16000)
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
                elif event.type == pygame.KEYDOWN:
                    if self.key_event is not None: threading.Thread(target=self.key_event, args=(event.key, 'began')).start()
                elif event.type == pygame.KEYUP:
                    if self.key_event is not None: threading.Thread(target=self.key_event, args=(event.key, 'ended')).start()
                else:
                    if self.window_dispatcher is not None: self.window_dispatcher()

            pygame.display.update()
            self.pygame_window.fill(self.bg)
            self.width = self.pygame_window.get_width()
            self.height = self.pygame_window.get_height()
            for elem in self.drawments:
                elem.on_draw(canvas=self.pygame_window)
                
        
        pygame.quit()
        
    def toggle_fullscreen(self, value: bool):
        if value:
            self.pygame_window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        else:
            self.pygame_window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.DOUBLEBUF)

    def show(self):
        self.window_process = threading.Thread(target=self._internal_main)
        self.window_process.start()
    
    def exit(self):
        sys.exit(0)