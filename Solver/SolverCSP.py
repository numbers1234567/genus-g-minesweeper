from Solver.SolverKnown import *
import numpy as np

class CSPSolverTile(SolverKnownTile):
    def __init__(self, id_, knowntype=SolverKnownTile.TYPECLOSED, neighbors=[], **kwargs):
        super().__init__(id_, knowntype=knowntype, neighbors=[neighbor for neighbor in neighbors], **kwargs)
        n_tiles_total = kwargs["n_tiles_total"]
        self.equation = np.array([0 for i in range(n_tiles_total+1)])
        self.unit_equation = np.array([0 for i in range(n_tiles_total+1)])

    """
    Add neighbor
    Update equation
    """
    def add_neighbor(self, other):
        super().add_neighbor(other)
        self.equation[other.id] = 1

    """
    Looks at own equation to determine what we can deduce. 
    For example:
        * Equation where every neighbor is a mine
        * Equation where every neighbor is not a mine

    Returns 1 for mine variables, 0 for nonmine variables, -1 for unknown
    """
    def eq_knowns(self):
        var_section = self.equation[:-1]
        if self.type != self.TYPEOPEN: return [-1 for i in var_section]
        # All mines
        if sum(var_section) == self.equation[-1]: return [1 if variable==1 else -1 for variable in var_section]
        # No mines
        if self.equation[-1] == 0: return [0 if variable==1 else -1 for variable in var_section]
        # All unknown
        return [-1 for i in var_section]

    """
    The same as the super update_tile, but does some operations ith the equation
    """
    def update_tile(self, tile_type, num_label=-1, force_update=False):
        old_state = self.type
        super().update_tile(tile_type, num_label)
        if old_state != self.type or force_update:
            if self.type  == self.TYPEOPEN:
                self.equation[-1] = num_label
                for tile in self.neighbors:
                    self.equation[tile.id] = 1
        if self.type == self.TYPEOPEN:
            self.unit_equation[-1] = 0
            self.unit_equation[self.id] = 1
        elif self.type == self.TYPEFLAG:
            self.unit_equation[self.id] = 1
            self.unit_equation[-1] = 1


"""
A very general implementation of CSP for any version of minesweeper.
Still doesn't have a proper definition of the neighbor_criteria class for subclasses
"""
class CSPSolver(SolverKnown):
    def __init__(self, tiletypes, solver_tile_class=CSPSolverTile, set_neighbors=True, **kwargs):
        super().__init__(tiletypes, solver_tile_class=solver_tile_class, set_neighbors=set_neighbors, **kwargs)
        for tile in self.tiles:
            tile.update_tile(tile.type, num_label=tile.num_label, force_update=True)

    """
    Performs a solve.
    Performs gaussian elimination to reduce the equations
    Returns whether or not a change was made
    """
    def next(self):
        made_update = False
        for tile in self.tiles:
            if tile.type != tile.TYPEOPEN: continue
            for other in self.tiles:
                if tile==other or other.type != other.TYPEOPEN: continue
                skip_elimination = False
                for i in range(len(tile.equation)-1):
                    if other.equation[i] == 1 and tile.equation[i] == 0: # Will result in a negative value
                        skip_elimination = True
                if skip_elimination: continue
                if np.sum(other.equation)==0: continue
                tile.equation -= other.equation
                made_update = True
                if skip_elimination: continue
        # Same thing with unit equation
        for tile in self.tiles:
            if tile.type != tile.TYPEOPEN: continue
            for other in self.tiles:
                if other.type != other.TYPEOPEN: continue
                skip_elimination = False
                for i in range(len(tile.equation)-1):
                    if other.unit_equation[i] == 1 and tile.equation[i] == 0: # Will result in a negative value
                        skip_elimination = True
                if skip_elimination: continue
                if np.sum(other.unit_equation)==0: continue
                tile.equation -= other.unit_equation
                made_update = True
                if skip_elimination: continue
        """for tile in self.tiles:
            print(tile.id)
            print(tile.equation)"""
        return made_update

    """
    Performs a solve then updates tile predictions
    """
    def predict(self):
        made_update = self.next()
        for tile in self.tiles:
            tile_knowns = tile.eq_knowns()
            for i in range(len(tile_knowns)):
                # Known
                if tile_knowns[i] == 1 or tile_knowns[i] == 0: self.tiles[i].next_prediction(tile_knowns[i])
        return made_update

    def get_predictions(self):
        return [tile.predict_type for tile in self.tiles]

    