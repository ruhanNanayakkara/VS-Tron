from graphics import egi, KEY
from pyglet import window
from pyglet.gl import *
from grid import Grid
from user import User
from audio import Audio
import time
from threading import Thread

GRID_SIZE = 50

def on_key_press(symbol, modifiers):
    global direction
    if symbol == KEY.LEFT or symbol == KEY.A:
        direction = 'left'
    elif symbol == KEY.RIGHT or symbol == KEY.D:
        direction = 'right'
    elif symbol == KEY.UP or symbol == KEY.W:
        direction = 'up'
    elif symbol == KEY.DOWN or symbol == KEY.S:
        direction = 'down'

if __name__ == '__main__':

    # create a pyglet window and set glOptions
    win = window.Window(width=GRID_SIZE * 10, height=GRID_SIZE * 10, vsync=True, resizable=False)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = window.FPSDisplay(win)
    # set fps limit
    FPS = 5

    # register key event handlers
    win.push_handlers(on_key_press)

    # create and initialise direction
    direction = ''
    # user list 
    users = []
    # add user(s)
    users.append(User(1, 25, 15, 50, 50, 'user'))
    users.append(User(2, 25, 35, 50, 50, 'minimax'))

    # create and initialise grid
    grid = Grid(GRID_SIZE, GRID_SIZE, users)

    # # media player
    # player = Audio('audio/Light Trails.mp3')

    # player.play()

    # run loop while no loss is detected
    while not grid.game_over:
        # start clock
        start = time.time()

        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # show nice FPS bottom right (default)
        # delta = clock.tick()

        grid.update(direction)
        grid.render()

        fps_display.draw()
        # swap the double buffer
        win.flip()
        # end clock
        end = time.time()
        # limit fps
        if ((1 / FPS) - (end - start) > 0):
            time.sleep((1 / FPS) - (end - start))
    
    for user in grid.eliminated:
        print("User " + str(user.colour) + " de-resolutioned!")