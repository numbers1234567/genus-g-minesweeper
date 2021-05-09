import pyglet
from msboard_genus_surfaces import *
from display_genus_board import *
from random import randint
from math import cos

"""
BOARD DEFINITION
"""
class Genus2Board(MSGenusGBoard):
    def __init__(self, mine_locs):
        super().__init__(mine_locs, 2)

class Genus2BoardGraphics(TileGraphicsContainer):
    OFFSET=(512,256)# Scale and then offset
    SCALE=20
    def __init__(self, tile, batch):
        tile_coords = [(coord[0]*self.SCALE+self.OFFSET[0], coord[1]*self.SCALE+self.OFFSET[1]) for coord in tile.coordinates]
        #print(tuple([*tile_coords[0],*tile_coords[1],*tile_coords[2]]))
        self.fill = batch.add(3, pyglet.gl.GL_TRIANGLES, None,
                              ("v2f", tuple([*tile_coords[0],*tile_coords[1],*tile_coords[2]])),
                              ("c3B", (0, 0, 255,0, 0, 255,0, 0, 255)))
        self.borders = batch.add(6, pyglet.gl.GL_LINES, None, 
                                 ("v2f", tuple([*tile_coords[0],*tile_coords[1],*tile_coords[1], *tile_coords[2], *tile_coords[2],*tile_coords[0]])),
                                 ("c3B", (255,255,255)*6))
        centroidX = sum([coord[0] for coord in tile_coords])/3
        centroidY = sum([coord[1] for coord in tile_coords])/3
        self.label = pyglet.text.Label(text=" ", font_size=18, anchor_x="center", anchor_y="center",x=int(centroidX), y=int(centroidY), batch=batch)
        self.label.font_size=12
        #self.label = pyglet.text.Label(text=" ", font_name="Calibri", font_size=24, x=512, y=256, batch=batch)
        self.tile = tile
        self.update_graphics()
    
    def update_graphics(self):
        if self.tile.revealed:
            self.fill.colors = [0, 0, 255,0, 0, 255,0, 0, 255]
            if self.tile.get_num_adjacent_mines != 0: self.label.text=str(self.tile.get_num_adjacent_mines())
            return
        if self.tile.flagged: self.fill.colors = [0,0,0,0,0,0,0,0,0]
        else: self.fill.colors = [150, 150, 150,150, 150, 150,150, 150, 150]

class GameContainer:
    CLICKREVEAL=1
    CLICKFLAG=2
    def __init__(self, mine_locs, board_type, graphics_container_type):
        self.display_batch = pyglet.graphics.Batch()
        self.board = board_type(mine_locs)
        self.graphics = [graphics_container_type(tile, self.display_batch) for tile in self.board.tiles]
    
    def display(self):
        for tile_graphics in self.graphics:
            tile_graphics.update_graphics()
        self.display_batch.draw()

    def on_click(self, x, y, type_):
        real_x=(x-self.graphics[0].OFFSET[0])/self.graphics[0].SCALE
        real_y=(y-self.graphics[0].OFFSET[1])/self.graphics[0].SCALE
        if type_==GameContainer.CLICKREVEAL: return (self.board.on_click(real_x, real_y, self.board.CLICKREVEAL))
        return self.board.on_click(real_x, real_y, self.board.CLICKFLAG)

class main(pyglet.window.Window):
    SCREENH=512
    SCREENW=1024
    def __init__(self, board_type):
        super().__init__(self.SCREENW, self.SCREENH)
        pyglet.gl.glClearColor(0,0,0,1)
        mine_locs = [randint(0, 4)==0 for i in range(800)]
        for i in range(8):mine_locs[i] = False
        self.game = GameContainer(mine_locs, Genus2Board, Genus2BoardGraphics)

    def on_draw(self):
        self.clear()
        self.game.display()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.game.on_click(x, y, GameContainer.CLICKREVEAL)
        if button == pyglet.window.mouse.RIGHT:
            self.game.on_click(x, y, GameContainer.CLICKFLAG)

if __name__=="__main__":
    window = main(Genus2Board)
    pyglet.app.run()