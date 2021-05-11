import pyglet
from msboard_genus_surfaces import *
from display_genus_board import *
from board_definitions import *
from screens.screen import *
from screens.game_screen import GameScreen
from random import randint
from math import cos
import sys

if __name__=="__main__":
    """board_type, board_graphics = genus_generate_compatible_class(int(sys.argv[1]))
    board_graphics.SCALE=40
    board_graphics.OFFSET = (512, 256)
    mine_locs = [randint(0, 4)==0 for i in range(int(sys.argv[1])*4*25)]
    for i in range(16):mine_locs[i] = False"""
    window = Main()
    pyglet.app.run()