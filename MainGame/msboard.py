
"""
Bare bones, general implementation of a Minesweeper tile
Contains the basic functions such as reveal (flood fill) and toggle_flag
"""
class MSTile:
    """
    Initializer for MSTile
     * bool hasmine - whether or not this tile contains a mine
     * int id - unique identifier for the tile
     * bool revealed - whether or not the tile is revealed. Default False
     * bool flagged - whether or not the tile is flagged. Default False
     * list neighbors - a default list of neighbors for the tile
    """
    def __init__(self, hasmine, id_, revealed=False, flagged=False, neighbors=[]):
        self.neighbors = neighbors
        self.hasmine = hasmine
        self.revealed = revealed
        self.flagged = flagged
        self.id = id_

    """
    Getters for the various attributes of the tile
    """
    def get_neighbors(self): return self.neighbors
    def get_hasmine(self): return self.hasmine
    def get_id(self): return self.id
    def get_isflagged(self): return self.flagged
    def get_num_adjacent_mines(self): return sum([1 if neighbor.hasmine else 0 for neighbor in neighbors])

    """
    Add and store MSTile other
    """
    def add_neighbor(self, other):
        if other in self.neighbors: return
        self.neighbors.append(other)

    """
    Reveals a tile and reveals all neighboring tiles if there are no mines around this one
    """
    def reveal(self):
        # Basic cases
        if self.hasmine: return False
        if self.revealed: return True
        # Recursive flood fill
        if self.num_adjacent_mines == 0: 
            for neighbor in self.neighbors: neighbor.reveal()
        
        return True

    """
    Toggle flag on tile
    """
    def toggle_flag(self):
        if self.revealed: return False
        self.flagged = not self.flagged
        return self.flagged

"""
Bare bones, general implementation of Minesweeper board
Subclasses must set what the criteria is for 2 neighboring tiles and implement the tile_at function
"""
class MSBoard:
    CLICKREVEAL = 1
    CLICKFLAG = 0
    """
    Initialize board.
    Parameters:
     * list tilelist_mine - A boolean list. Basically an id - is_a_mine dictionary.
     * class tile_class - The name of a subclass of MSTile to be used by the class
    """
    def __init__(self, tilelist_mine, tile_class=MSTile):
        self.tiles=[tile_class(tilelist_mine[i], i) for i in range(len(tilelist_mine))]
        # Set up neighbors
        for tile in self.tiles:
            for other in self.tiles:
                if tile==other: continue
                if neighbor_criteria(tile, other):
                    tile.add_neighbor(other)
                    other.add_neighbor(tile)

    """
    Returns whether or not tile1 and tile2 are neighbors
    Parameters:

    """
    def neighbor_criteria(self, tile1, tile2):
        pass

    def tile_at(self, x, y):
        pass

    """
    Process a single click.
    Parameters:
     * float x & y: The point of the click
     * 
    """
    def on_click(self, x, y, clicktype):
        return self.on_click_reveal(x, y) if clicktype==self.CLICKREVEAL else self.on_click_toggleflag(x, y)
    # Helper functions for the on_click function which can be overwritten for extra functionality
    def on_click_toggleflag(self, x, y): return self.tile_at(x, y).toggle_flag()
    def on_click_reveal(self, x, y): return self.tile_at(x, y).reveal()