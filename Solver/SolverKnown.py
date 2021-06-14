
"""
This is very much based on the MSBoard but designed to be easily interfaced
"""
class SolverKnownTile(self):
    TYPEFLAG = -1
    TYPECLOSED = -2
    """
    class attributes:
        list neighbors: A list of neighbors of type SolverKnownTile
        int self.type: TYPEFLAG if flag, TYPECLOSED if closed, otherwise it is the known number of mines around it
        int self.id: index of tile for future computations
        int self.predict_type: The type of the tile after logical steps by the solver. Default has the same value as self.type
    """
    def __init__(self, id_, n_tiles_total, knowntype=SolverKnownTile.TYPECLOSED, neighbors=[]):
        self.neighbors = [tile for tile in neighbors]
        self.type = knowntype
        self.id = id_
        self.predict_type = self.type
        self.equation = [0 for i in range(n_tiles_total+1)]

    def add_neighbor(self, other):
        if other not in self.neighbors: self.neighbors.append(other)
        self.equation[other.id_] = 1

    def next_prediction(self, prediction_type):
        self.predict_type = prediction_type

class SolverKnown:
    def __init__(self, tiletypes, solver_tile_class=SolverKnownTile, set_neighbors=True):
        self.tiles = [solver_tile_class(id_=i, knowntype=tiletypes[i]) for i in range(len(tiletypes))]
        if set_neighbors:
            self.setup_neighbors()

    """
    Main logical function to be overridden
    """
    def predict(self):
        pass
    
    """
    A way to determine if 2 tiles are neighbors. Meant to be overridden
    """
    def neighbor_criteria(self, tile1, tile2):
        pass

    def setup_neighbors(self):
        for tile in self.tiles:
            for other in self.tiles:
                if tile==other: continue
                if self.neighbor_criteria(tile, other):
                    tile.add_neighbor(other)
                    other.add_neighbor(tile)
