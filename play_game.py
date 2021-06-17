import pyglet
from MainGame.msboard_genus_surfaces import *
from MainGame.display_genus_board import *
from MainGame.board_definitions import *
from MainGame.screens.game_screen import GameScreen
from MainGame.screens.main_menu import MainMenu
from random import randint
from math import cos
import sys

board_type, board_graphics = genus_generate_compatible_class(int(sys.argv[1]))
board_graphics.SCALE=40
board_graphics.OFFSET = (512, 256)
mine_locs = [randint(0, 4)==0 for i in range(int(sys.argv[1])*4*25)]
for i in range(16):mine_locs[i] = False

class Main(pyglet.window.Window):
    SCREENH=512
    SCREENW=1024
    def __init__(self, board_type, board_graphics, num_tiles, num_mines):
        super().__init__(self.SCREENW, self.SCREENH)
        pyglet.gl.glClearColor(0,0,0,1)
        self.current_screen = GameScreen([False for i in range(num_tiles)], board_type, board_graphics)
        self.board_type = board_type
        self.board_graphics = board_graphics
        self.num_tiles = num_tiles
        self.num_mines = num_mines
        self.waiting_first_click = True

    def on_draw(self):
        self.current_screen.display(self)

    def on_mouse_press(self, x, y, button, modifiers):
        self.current_screen.on_click(x, y, button, modifiers)
        if self.waiting_first_click:
            for tile in self.current_screen.game.board.tiles:
                if tile.revealed:
                    mine_locs = load_random_board(self.board_type, self.num_tiles, self.num_mines, firstclick_id=tile.id)
                    tile_id = tile.id
                    self.waiting_first_click=False
                    self.current_screen = GameScreen(mine_locs, self.board_type, self.board_graphics)
                    self.current_screen.game.board.tiles[tile_id].reveal()
                    break

    def set_screen(self, new_screen):
        self.current_screen = new_screen

    def on_key_press(self, symbol, modifiers):
        self.current_screen.on_key_press(symbol, modifiers)

if __name__=="__main__":
    """board_type, board_graphics = genus_generate_compatible_class(int(sys.argv[1]))
    board_graphics.SCALE=40
    board_graphics.OFFSET = (512, 256)
    mine_locs = [randint(0, 4)==0 for i in range(int(sys.argv[1])*4*25)]
    for i in range(16):mine_locs[i] = False"""
    board_type, board_graphics = genus_generate_compatible_class(int(sys.argv[1]))
    board_graphics.SCALE=40
    board_graphics.OFFSET=(512, 256)


    window = Main(board_type, board_graphics, int(sys.argv[2]), int(sys.argv[3]))
    pyglet.app.run()