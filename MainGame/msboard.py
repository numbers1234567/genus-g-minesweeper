
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
        self.neighbors = [neigh for neigh in neighbors]
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
        self.revealed = True
        if True not in [neighbor.hasmine for neighbor in self.neighbors]: 
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
                if self.neighbor_criteria(tile, other):
                    tile.add_neighbor(other)
                    other.add_neighbor(tile)

    """
    Returns whether or not tile1 and tile2 are neighbors
    Parameters:

    """
    def neighbor_criteria(self, tile1, tile2):
        return abs(tile1.id-tile2.id)==1

    def tile_at(self, x, y):
        pass

    """
    Process a single click.
    Parameters:
     * float x & y: The point of the click
     * 
    """
    def on_click(self, x, y, clicktype):
        return self.on_click_reveal(self.tile_at(x, y)) if clicktype==self.CLICKREVEAL else self.on_click_toggleflag(self.tile_at(x, y))
    # Helper functions for the on_click function which can be overwritten for extra functionality
    def on_click_toggleflag(self, tile): return tile.toggle_flag()
    def on_click_reveal(self, tile): return tile.reveal()

if __name__=="__main__": # TESTS
    from random import randint
    print("=========\nTESTING MINELIST\n=========")
    minelst = [True if randint(0,1)==0 else False for i in range(100)]
    print("Mine list: " + str(minelst))
    board = MSBoard(minelst)
    # Is valid?
    print("Correct mine positions: " + str(not (False in [minelst[i] == board.tiles[i].hasmine for i in range(len(minelst))])))
    # Test clicking
    print("Tile 0 has mine: " + str(board.tiles[0].hasmine))
    print("Result of tile 0 click: " + str(board.on_click_reveal(board.tiles[0])))
    # Test clicking
    print("=========\nTESTING CLICKING\n=========")
    minelst = [False for i in range(100)]
    minelst[10] = True
    board = MSBoard(minelst)
    print("Tile 5 neighbors: " + str([neighbor.id for neighbor in board.tiles[5].get_neighbors()]))
    print("Tile 5 reveal: " + str(board.on_click_reveal(board.tiles[5])))
    print("Reveal list: " + str([tile.revealed for tile in board.tiles]))
