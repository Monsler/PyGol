import pygame
from pygol import ui
import warnings
import copy, math

class Drawable:
    width = None
    height = None
    x = None
    y = None
    visible = True
    instance = None

    def created(self):
        pass

    def on_draw(self, canvas: pygame.Surface):
        pass

    def destroyed(self):
        pass

    def remove_self(self):
        pass

    def clicked(self, canvas: pygame.Surface, phase: str, pos, event):
        pass

    def rotate(self, angle: float):
        pass


class Rect(Drawable):
    def __init__(self, x: int, y: int, width: int, height: int, color=(255, 0, 0)) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.parent = None
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.click_listener = None
        self.visible = True
        self.instance = self.rect
        self._rounded = 0
        self.angle = 0

    def set_round_value(self, value: int):
        self._rounded = value

    def on_draw(self, canvas: pygame.Surface):
        if self.visible:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(canvas, self.color, self.rect, self._rounded, self._rounded)

    def set_click_listener(self, listener):
        self.click_listener = listener

    def remove_self(self):
        if self in self.parent.drawments:
            self.parent.drawments.remove(self)
            self = None
        else:
            warnings.warn('I dont have a parent!')
    
    def clicked(self, canvas: pygame.Surface, phase: str, pos, event):
        if self.rect.collidepoint(pos) and self.visible:
            if self.click_listener is not None: self.click_listener(phase, canvas, self, event)

class Image(Drawable):
    def __init__(self, x: int, y: int, image: str) -> None:
        self.image = pygame.image.load(image)
        self._img = copy.copy(self.image)
        self.x = x
        self.y = y
        self.converted = False
        self.visible = True
        self.click_listener = None
        self.angle = 0
        self.instance = self.image

    def rotate(self, angle: float):
        self.angle = angle
        self.image = pygame.transform.rotate(self._img, self.angle)

    def scale(self, width: int, height: int):
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self._img, (width, height))
        self._img = copy.copy(self.image)

    def set_click_listener(self, listener):
        self.click_listener = listener

    def on_draw(self, canvas: pygame.Surface):
        if not self.converted:
            self.image.convert()
            self.converted = True
        if self.visible:
            canvas.blit(self.image, (self.x, self.y))
    
    def clicked(self, canvas: pygame.Surface, phase: str, pos, event):
        if self.image.get_rect().collidepoint(pos) and self.visible:
            if self.click_listener is not None: self.click_listener(phase, canvas, self, event)

class Circle(Drawable):
    def __init__(self, color=(0, 0, 0), width=0, radius=3, x=0, y=0) -> None:
        self.width = width
        self.radius = radius
        self.color = color
        self.visible = True
        self.x = x
        self.y = y
        self.click_listener = None
    
    def set_click_listener(self, listener):
        self.click_listener = listener

    def clicked(self, canvas: pygame.Surface, phase: str, pos, event):
        if math.sqrt((pos[0]-self.x+self.radius)**2+(pos[1]-self.y+self.radius)**2) <= self.radius and self.visible: 
            if self.click_listener is not None: self.click_listener(phase, canvas, self, event)
    
    def on_draw(self, canvas: pygame.Surface):
        if self.visible:
            pygame.draw.circle(canvas, self.color, (self.x, self.y), self.radius, self.width)

class Text(Drawable):
    def __init__(self, label, fontname, size, x=0, y=0, color=(0, 0, 0)) -> None:
        self.x = x
        self.y = y
        self.text = label
        self.color = color
        self.font_name = fontname
        self.font = pygame.font.SysFont(fontname, size)
        self.label = self.font.render(self.text, False, self.color)
        self.visible = True
    
    def get_size(self) -> int:
        return self.font.size(self.text)

    def set_text(self, text: str):
        self.text = text
        self.label = self.font.render(self.text, False, self.color)
    
    def on_draw(self, canvas: pygame.Surface):
        if self.visible:
            canvas.blit(self.label, (self.x, self.y))

class Group(Drawable):
    def __init__(self, x: int=0, y: int=0, width: int=150, height: int=150) -> None:
        self.width = width
        self.height = height
        self.canvas = pygame.Surface((width, height), pygame.SRCALPHA)
        self._canvas = copy.copy(self.canvas)
        self.x = x
        self.y = y
        self.angle = 0
        self.drawments = []
    
    def insert(self, of: Drawable):
        self.drawments.append(of)
        of.on_draw(canvas=self.canvas)
        self._canvas = copy.copy(self.canvas)
        of.parent = self
    
    def repaint(self):
         self._canvas = copy.copy(self.canvas)

    def rotate(self, angle: float):
        self.angle = angle
        self.canvas = pygame.transform.rotate(self._canvas, self.angle)

    def remove_self(self):
        self.parent.drawments.remove(self)
        del self

    def on_draw(self, canvas: pygame.Surface):
        canvas.blit(self.canvas, (self.x, self.y))
        for elem in self.drawments:
                elem.on_draw(canvas=self.canvas)
            