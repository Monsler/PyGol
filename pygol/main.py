from pygol import ui, drawable
from pygol import routine
import time
win = ui.Window()

def tf_listener(key, phase, target):
    val: str = target.value
    if phase == 'ended':
        if val.isdigit() and 6 < int(target.value) < 8:
            target.placeholder_text = 'Congratulations!'
            target.value = ''
            target.locked = True
        else:
            target.placeholder_text = 'Try again!'
            target.value = ''

if __name__ == '__main__':
    win.show()
    win.bg = (100, 100, 100)
    tf = drawable.TextField('What stays between six and eight? (type a number)', 10, 185, win.width-20, 30, 's.ttf')
    #tf.locked = True
    
    tf.listener = tf_listener
    win.insert(tf)