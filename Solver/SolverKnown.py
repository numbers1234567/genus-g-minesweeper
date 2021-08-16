"""
This is very much based on the MSBoard but designed to be easily interfaced
"""
class SolverKnownTile:
    TYPEFLAG = 1
    TYPECLOSED = 2
    TYPEOPEN = 0
    """
    class attributes:
        list neighbors: A list of neighbors of type SolverKnownTile
        int self.type: TYPEFLAG if flag, TYPECLOSED if closed, otherwise it is the known number of mines around it
        int self.id: index of tile for future computations
        int self.predict_type: The type of the tile after logical steps by the solver. Default has the same value as self.type
    """
    def __init__(self, id_, knowntype=None, neighbors=[], **kwargs):
        this_known_type = knowntype
        if knowntype == None:
            this_known_type = self.TYPECLOSED
        self.neighbors = [tile for tile in neighbors]
        self.type = this_known_type
        self.id = id_
        self.predict_type = self.type
        self.num_label = -1

    """
    Add SolverKnownTile other into the list of neighbors
    """
    def add_neighbor(self, other):
        if other not in self.neighbors: self.neighbors.append(other)

    """
    Update the labeling of this tile
    """
    def next_prediction(self, prediction_type):
        self.predict_type = prediction_type

    def update_num_label(self, num_label):
        self.num_label = num_label

    def update_tile(self, tile_type, num_label=-1):
        self.type = tile_type
        self.num_label = num_label
        self.next_prediction(tile_type)

class SolverKnown:
    def __init__(self, tiletypes, solver_tile_class=SolverKnownTile, set_neighbors=True, **kwargs):
        self.tiles = [solver_tile_class(id_=i, knowntype=tiletypes[i], **kwargs) for i in range(len(tiletypes))]
        if set_neighbors:
            self.setup_neighbors()

    def next(self):
        pass

    """
    Main logical function to be overridden.
    Updates tiles by calling next_prediction
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
    """
    Updates tile labelling.
    The input is a list of integers, indices corresponding to ids. -2 for unknown, -1 for flag, any nonnegative integer indicates number of surrounding mines.
    """
    def update(self, labels):
        for i in range(len(labels)):
            if labels[i] >= 0: 
                self.tiles[i].update_tile(self.tiles[i].TYPEOPEN, labels[i])
            elif labels[i] == -self.tiles[i].TYPEFLAG:
                self.tiles[i].update_tile(self.tiles[i].TYPEFLAG)
            elif labels[i] == -self.tiles[i].TYPECLOSED:
                self.tiles[i].update_tile(self.tiles[i].TYPECLOSED)
    """
    Returns the current known predictions of the solver
    """
    def get_predictions(self):
        return [tile.predict_type for tile in self.tiles]

if __name__=="__main__":
    SolverKnown([])