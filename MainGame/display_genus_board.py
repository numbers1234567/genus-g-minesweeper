import pyglet
import numpy as np
from MainGame.msboard_genus_surfaces import *
import time
from math import sqrt

class TileGraphicsContainer:
    OFFSET=(0, 0)
    SCALE=1
    def __init__(self, tile, batch): # Force an implementation
        pass

    def update_graphics(self):
        pass

if __name__=="__main__":
    batch = pyglet.graphics.Batch()
    board = MSGenusGBoard([False for i in range(80000)], 2)
    test_tile = board.tiles[11]
    numsides = 8
    tile_graphics = TileGraphicsContainer(board.tiles[0], batch, 2)