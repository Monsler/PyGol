# PyGol
PyGol is a pure python library which is based on pygame and simplifies its functions.
Heavily inspired by Solar2D
<br>
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
    text.x = (win.pygame_window.get_width()/2)-(text.get_size()[0]/2)
    text.y = (win.pygame_window.get_height()/2)-(text.get_size()[1]/2)

# Perform with delay: 10 millis; function: update; repeats: 0
perform_with_delay(10, update, 0)
```
