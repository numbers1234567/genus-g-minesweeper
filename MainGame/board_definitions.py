from pyglet.gl import GL_TRIANGLES, GL_LINES
from pyglet.text import Label as pyglLabel
from MainGame.display_genus_board import *

"""
Generate the minesweeper board subclass with the given genus.
Returns a tuple of form (tile graphics type, board type).
"""
def genus_generate_compatible_class(genus):
    """Generate graphics class"""
    class GenusGBoardGraphics(TileGraphicsContainer):
        def __init__(self, tile, batch, text_batch):
            # Get screen coordinates
            self.tile_coords = [(coord[0]*self.SCALE+self.OFFSET[0], coord[1]*self.SCALE+self.OFFSET[1]) for coord in tile.coordinates]
            # Store batches
            self.batch = batch
            self.text_batch = text_batch
            # Skeleton
            self.fill = batch.add(3, GL_TRIANGLES, None,
                                ("v2f", tuple([*self.tile_coords[0],*self.tile_coords[1],*self.tile_coords[2]])),
                                ("c3B", (0, 0, 255,0, 0, 255,0, 0, 255)))
            self.borders = batch.add(6, GL_LINES, None, 
                                    ("v2f", tuple([*self.tile_coords[0],*self.tile_coords[1],*self.tile_coords[1], *self.tile_coords[2], *self.tile_coords[2],*self.tile_coords[0]])),
                                    ("c3B", (255,255,255)*6))

            self.label = None
            self.tile = tile
            self.update_graphics()
        
        def update_graphics(self):
            if self.tile.revealed:
                self.fill.colors = [0, 0, 255,0, 0, 255,0, 0, 255]
                if self.tile.get_num_adjacent_mines() > 0 and self.label==None: 
                    centroidX = sum([coord[0] for coord in self.tile_coords])/3
                    centroidY = sum([coord[1] for coord in self.tile_coords])/3
                    self.label = pyglLabel(text=str(self.tile.get_num_adjacent_mines()), font_size=18, anchor_x="center", anchor_y="center",x=int(centroidX), y=int(centroidY), batch=self.text_batch)
                    self.label.font_size=12
                return
            if self.tile.flagged: self.fill.colors = [0,0,0,0,0,0,0,0,0]
            else: self.fill.colors = [150, 150, 150,150, 150, 150,150, 150, 150]
    
    class GenusGBoard(MSGenusGBoard):
        def __init__(self, mine_locs):
            super().__init__(mine_locs, genus)
    
    return (GenusGBoard, GenusGBoardGraphics)