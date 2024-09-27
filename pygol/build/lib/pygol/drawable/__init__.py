import pygame
import warnings
import copy, math, os, time, threading

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
        self.click_listener = None
    
    def clicked(self, canvas: pygame.Surface, phase: str, pos, event):
        if self.label.get_rect(topleft=(self.x, self.y)).collidepoint(pos) and self.visible:
            if self.click_listener is not None: self.click_listener(phase, canvas, self, event)
    
    def set_file_font(self, path: str, size: int):
        if os.path.exists(path):
            self.font = pygame.font.Font(path, size)
        else:
            raise OSError(f'Path {path} does not exist!')

    def set_click_listener(self, listener):
        self.click_listener = listener
    
    def get_size(self) -> int:
        return self.font.size(self.text)

    def set_text(self, text: str):
        self.text = text
        self.label = self.font.render(self.text, True, self.color)
    
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
        if not of in self.drawments:
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

class TextField(Drawable):
    def __init__(self, placeholder: str, x: int, y: int, width: int, height: int, font: str) -> None:
        self.placeholder_text = placeholder
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = ''
        self.bg = (0, 0, 0)
        self.fg = (255, 255, 255)
        self.group = Group(self.x, self.y, self.width, self.height)
        self.text = Text(self.placeholder_text, None, 0, 7, 0, (175, 175, 175))
        self.text.set_file_font(font, int(self.height/2))
        self.text.set_text(placeholder)
        self.text.y = self.height/2 - self.text.get_size()[1]/2 - 1
        self.background = Rect(0, 0, self.width+self.text.get_size()[0], self.height, self.bg)
        self.group.insert(self.background)
        self.group.insert(self.text)
        self.caps = False
        self.use_line = True
        self.previous_key = pygame.K_0
        self.listener = None
        self.locked = False
        threading.Thread(target=self.__use__line__, daemon=True, args=()).start()

    
    def clicked(self, canvas: pygame.Surface, phase: str, pos, event):
        if self.group.canvas.get_rect(topleft=(self.x, self.y)).collidepoint(pos) and phase == 'began' and not self.locked:
            self.parent.textfield = self
            self.parent.tf_evt = self.key
            self.use_line = True
        
    def __use__line__(self):
        while True:
            time.sleep(0.6)
            self.use_line = not self.use_line
    
    def key(self, key):
        if key != pygame.K_BACKSPACE:
            if key == pygame.K_SPACE:
                self.value += ' '
            elif key == pygame.K_LSHIFT:
                self.previous_key = key
            elif key == pygame.K_CAPSLOCK:
                self.caps = not self.caps
            elif key == pygame.K_RETURN:
                self.parent.reset_focus()
                if self.listener is not None: self.listener(key, 'ended', self)
            elif key == pygame.K_DELETE and self.previous_key == pygame.K_LSHIFT:
                self.value = ''
            elif key == pygame.K_1 and self.previous_key == pygame.K_LSHIFT:
                self.value += '!'
                self.previous_key = pygame.K_0
                if self.listener is not None: self.listener(key, 'changed', self)
            elif key == pygame.K_2 and self.previous_key == pygame.K_LSHIFT:
                self.value += '@'
                self.previous_key = pygame.K_0
                if self.listener is not None: self.listener(key, 'changed', self)
            elif key == pygame.K_3 and self.previous_key == pygame.K_LSHIFT:
                self.value += '#'
                self.previous_key = pygame.K_0
                if self.listener is not None: self.listener(key, 'changed', self)
            elif key == pygame.K_4 and self.previous_key == pygame.K_LSHIFT:
                self.value += '$'
                self.previous_key = pygame.K_0
                if self.listener is not None: self.listener(key, 'changed', self)
            elif key == pygame.K_5 and self.previous_key == pygame.K_LSHIFT:
                self.value += '%'
                self.previous_key = pygame.K_0
                if self.listener is not None: self.listener(key, 'changed', self)
            elif key == pygame.K_6 and self.previous_key == pygame.K_LSHIFT:
                self.value += '^'
                self.previous_key = pygame.K_0
                if self.listener is not None: self.listener(key, 'changed', self)
            elif key == pygame.K_7 and self.previous_key == pygame.K_LSHIFT:
                self.value += '&'
                self.previous_key = pygame.K_0
                if self.listener is not None: self.listener(key, 'changed', self)
            elif key == pygame.K_8 and self.previous_key == pygame.K_LSHIFT:
                self.value += '*'
                self.previous_key = pygame.K_0
                if self.listener is not None: self.listener(key, 'changed', self)
            elif key == pygame.K_9 and self.previous_key == pygame.K_LSHIFT:
                self.value += '('
                self.previous_key = pygame.K_0
                if self.listener is not None: self.listener(key, 'changed', self)
            elif key == pygame.K_0 and self.previous_key == pygame.K_LSHIFT:
                self.value += ')'
                self.previous_key = pygame.K_0
                if self.listener is not None: self.listener(key, 'changed', self)
            elif key == pygame.K_SEMICOLON and self.previous_key == pygame.K_LSHIFT:
                self.value += ':'
                self.previous_key = pygame.K_0
                if self.listener is not None: self.listener(key, 'changed', self)
            elif key == pygame.K_RIGHT and self.previous_key == pygame.K_LSHIFT:
                self.value = self.value[1:len(self.value)]
                if self.listener is not None: self.listener(key, 'changed', self)
            else:
                self.value += pygame.key.name(key) if self.caps == False else pygame.key.name(key).upper()
                self.previous_key = pygame.K_0
                if self.listener is not None: self.listener(key, 'changed', self)
        else:
            self.value = self.value[0:len(self.value)-1]
        
        self.use_line = True
        

    def on_draw(self, canvas: pygame.Surface):
        self.group.on_draw(canvas)
        self.background.color = self.bg
        if self.parent.textfield == self:
            if self.use_line:
                self.text.set_text(self.value+'|')
            else:
                self.text.set_text(self.value)
            self.text.color = self.fg
            self.group.repaint()
        else:
            if self.value == '':
                self.text.set_text(self.placeholder_text)
                self.text.color = (175, 175, 175)
                self.group.repaint()
            else:
                self.text.set_text(self.value)
                self.text.color = self.fg
                self.group.repaint()
        
        if self.locked:
            self.group.canvas.set_alpha(150)