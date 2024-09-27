# PyGol
PyGol is a pure python library which is based on pygame and simplifies its functions.
Heavily inspired by Solar2D<br>
# How to install?

```
pip install pygol-engine
```
<img src="https://i.ibb.co/HDs3gLB/1.png"><br>
Hello World Example:

```python
from pygol.ui import Window
from pygol.drawable import Text
from pygol.routine import perform_with_delay

win = Window(width=400, height=400)
win.show()
text = Text('Hello, world!', 'Comic Sans MS', 60, 0, 5, (0, 0, 0))
win.insert(text)

#Update function
def update():
    if win.pygame_window != None:
        text.x = (win.pygame_window.get_width()/2)-(text.get_size()[0]/2)
        text.y = (win.pygame_window.get_height()/2)-(text.get_size()[1]/2)

# Perform with delay: 10 millis; function: update; repeats: 0
perform_with_delay(10, update, 0)
```

Rotating rectange example:

```python
from pygol.ui import Window
from pygol.drawable import Rect, Group
from pygol.routine import perform_with_delay

win = Window(width=700, height=400, title='Example')
g = Group(225, 70, 200, 200)
r1 = Rect(0, 0, 100, 200)

global angle
angle = 0

def rotate():
    global angle
    g.rotate(angle)
    angle += 1

if __name__ == '__main__':
    win.bg = (0, 0, 0)
    win.show()
    win.insert(g)
    r2 = Rect(100, 0, 100, 200, (0, 0, 255))
    g.insert(r1)
    g.insert(r2)
    

    perform_with_delay(10, rotate, 0)
```
