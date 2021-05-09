import pyglet
from msboard_genus_surfaces import *
from display_genus_board import *
from board_definitions import *
from random import randint
from math import cos
import sys

"""
Main game container
"""
class Game:
    CLICKREVEAL=1
    CLICKFLAG=2
    def __init__(self, mine_locs, board_type, graphics_container_type):
        self.display_batch = pyglet.graphics.Batch()
        self.text_batch = pyglet.graphics.Batch()
        self.board = board_type(mine_locs)
        self.graphics = [graphics_container_type(tile, self.display_batch, self.text_batch) for tile in self.board.tiles]
    
    def display(self):
        for tile_graphics in self.graphics:
            tile_graphics.update_graphics()
        self.display_batch.draw()
        self.text_batch.draw()

    def on_click(self, x, y, type_):
        real_x=(x-self.graphics[0].OFFSET[0])/self.graphics[0].SCALE
        real_y=(y-self.graphics[0].OFFSET[1])/self.graphics[0].SCALE
        if type_==Game.CLICKREVEAL: return (self.board.on_click(real_x, real_y, self.board.CLICKREVEAL))
        return self.board.on_click(real_x, real_y, self.board.CLICKFLAG)

class Main(pyglet.window.Window):
    SCREENH=512
    SCREENW=1024
    def __init__(self, board_type, board_graphics, mine_locs):
        super().__init__(self.SCREENW, self.SCREENH)
        pyglet.gl.glClearColor(0,0,0,1)
        self.game = Game(mine_locs, board_type, board_graphics)

    def on_draw(self):
        self.clear()
        self.game.display()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.game.on_click(x, y, Game.CLICKREVEAL)
        if button == pyglet.window.mouse.RIGHT:
            self.game.on_click(x, y, Game.CLICKFLAG)

if __name__=="__main__":
    board_type, board_graphics = genus_generate_compatible_class(int(sys.argv[1]))
    board_graphics.SCALE=20
    board_graphics.OFFSET = (512, 256)
    mine_locs = [randint(0, 4)==0 for i in range(int(sys.argv[1])*4*25)]
    for i in range(16):mine_locs[i] = False
    window = Main(board_type, board_graphics, mine_locs)
    pyglet.app.run()