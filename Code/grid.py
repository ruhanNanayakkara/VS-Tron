from graphics import egi
import pyglet
from pyglet.gl import *
from point2d import Point2D
from user import User

COLOURS = {
    0 : (0.0, 0.0, 0.0, 1.0), # black, grid colour
    1 : (0.0, 0.0, 1.0, 1.0), # blue, player 1 trail
    2 : (1.0, 1.0, 0.0, 1.0), # yellow, player 2 trail
    3 : (1.0, 0.7, 0.0, 1.0), # orange, player 3 trail
    4 : (1.0, 0.0, 0.0, 1.0), # red, player 4 trail
    5 : (1.0, 1.0, 1.0, 1.0) # white, walls
}

class Grid(object) :
    def __init__(self, r, c, users):
        self.rows = r
        self.columns = c
        self.dimensions = 10
        self.grid = []

        # all users in grid
        self.users = users
        # number of users in grid
        self.user_count = len(users)

        # variable to check if game is over
        self.game_over = False
        # list of eliminated users
        self.eliminated = []
        
        # initialise grid
        for i in range(r):
            other = []
            for j in range(c):
                if i == 0 or i == self.rows - 1:
                    other.append(5)
                elif j == 0 or j == self.columns - 1:
                    other.append(5)
                else:
                    other.append(0)
            self.grid.append(other)

        # change players' positions in grid to their colour
        for user in users:
            self.grid[user.row][user.column] = user.colour

    def draw_grid(self):
        for r in range(self.rows):
            for c in range(self.columns):
                # check if cell is occupied
                if self.grid[r][c] != 0:
                    # set pen colour to player's colour
                    egi.set_pen_color(COLOURS[self.grid[r][c]])
                    points = (
                        Point2D(c * self.dimensions, (r + 1) * self.dimensions), # top left
                        Point2D((c + 1) * self.dimensions, (r + 1) * self.dimensions), # top right
                        Point2D((c + 1) * self.dimensions, r * self.dimensions), # bottom right
                        Point2D(c * self.dimensions, r * self.dimensions) # bottom left
                    )
                    # draw cell
                    egi.closed_shape(points, True)
                    
    def update(self, direction = ""):
        eliminated = False
        if direction != "":
            for i in range(len(self.users)):
                user = self.users[i]
                if i == 0 and len(self.users) > 1:
                    crash = user.update(self.users[1], self.grid, direction)
                else:
                    crash = user.update(self.users[0], self.grid, direction)
                if crash:
                    self.eliminated.append(user)
                    eliminated = True
                    # game is over if only one player remians in grid
                    if len(self.eliminated) == (self.user_count - 1):
                        self.game_over = True
            # check if a player has been eliminated
            if eliminated:
                for user in self.eliminated:
                    # remove each player that has been eliminated
                    if user in self.users:
                        self.users.remove(user)

    def render(self):
        self.draw_grid()
