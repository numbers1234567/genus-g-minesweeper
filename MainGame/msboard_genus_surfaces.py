import msboard
from math import sin, cos, pi, sqrt, ceil
import numpy as np
import time

"""
Basic helpers
"""
def rotate2d(vec, theta):
    return (cos(theta)*vec[0]-sin(theta)*vec[1], sin(theta)*vec[0]+cos(theta)*vec[1])

def area_triangle(coords):
    return abs(coords[0][0]*(coords[1][1]-coords[2][1])+
               coords[1][0]*(coords[2][1]-coords[0][1])+
               coords[2][0]*(coords[0][1]-coords[1][1]))/2.

def round_hundredths(num):
    return round(num*100)/100

def shift_vector(vec, off):
    return [vec[i]+off[i] for i in range(len(vec))]

"""
Implemented genus g tile with geometric helper functions to aid in computation
"""
class MSGenusG(msboard.MSTile):
    def __init__(self, hasmine, id_, revealed=False, flagged=False, neighbors=[], genus=2):
        super().__init__(hasmine, id_, revealed=revealed, flagged=flagged, neighbors=neighbors)
        self.coordinates = [0,0]
        self.genus=genus

    """
    Takes the genus of the surface and returns out the coordinates of this tile when
    the surface is mapped to a regular polygon
    """
    def get_triangle_coordinates(self):
        genus = self.genus
        numsides = genus*4
        large_angle = (pi-2*pi/numsides)/2
        triangle_height = sin(large_angle)
        triangle_width = 2*cos(large_angle)
        # (sector, row, column)
        row = int(sqrt(self.id/numsides))
        sector = int((self.id-numsides*(row**2))/(2*row+1))
        column = (self.id-numsides*(row**2))%(2*row+1)
        # Base for the coordinates
        coordinates_base = [[0, 0], 
                            [cos(large_angle), sin(large_angle)], 
                            [-cos(large_angle), sin(large_angle)]]
        if column%2==1: coordinates_base = [[0, sin(large_angle)], [-cos(large_angle), 0], [cos(large_angle), 0]]
        coordinates_base = [shift_vector(coord, [(column-row)*cos(large_angle), row*sin(large_angle)]) for coord in coordinates_base]
        # Rotate to sector
        rotation_a = -2*pi*sector/numsides
        return [tuple([round_hundredths(dim) for dim in rotate2d(vec, rotation_a)]) for vec in coordinates_base]

"""
Implementation of genus g board
"""
class MSGenusGBoard(msboard.MSBoard):
    def __init__(self, mine_locs, genus):
        self.genus = genus
        self.numrows = int(sqrt(len(mine_locs)/(4*genus)))+1
        super().__init__(mine_locs, tile_class=MSGenusG)

    def neighbor_criteria(self, tile1, tile2):
        for coord1 in tile1.coordinates:
            for coord2 in tile2.coordinates:
                if False not in list(coord1==coord2): return True

    def setup_neighbors(self):
        # Set up coordinates
        times=[]
        for tile in self.tiles: 
            tile.genus = self.genus
            tile.coordinates = tile.get_triangle_coordinates()
        coords = {}
        # Figure out shared points
        for tile in self.tiles:
            tile_coords = tile.coordinates
            for coord in tile_coords:
                try: coords[coord].append(tile)
                except KeyError: coords[coord] = [tile]
        # Neighborize tiles sharing points
        for coord in list(coords.keys()):
            for tile in coords[coord]:
                for other in coords[coord]:
                    if other==tile:continue
                    tile.add_neighbor(other)
                    other.add_neighbor(other)
        # Glue edges together
        columns_final = 2*self.numrows-1
        glue_start=(4*self.genus)*((self.numrows-1)**2)
        for start in range(glue_start, len(self.tiles), 4*columns_final):
            first = []
            second = []
            for from_ in range(1, columns_final, 2):
                first.append(self.tiles[start+from_].coordinates[0])
                second.append(self.tiles[start+3*columns_final-1-from_].coordinates[0])
                first.append(self.tiles[start+from_+columns_final].coordinates[0])
                second.append(self.tiles[start+4*columns_final-1-from_].coordinates[0])
            for i in range(len(first)):
                for tile1 in coords[first[i]]+coords[second[i]]:
                    for tile2 in coords[first[i]]+coords[second[i]]:
                        if tile1==tile2: continue
                        tile1.add_neighbor(tile2)
                        tile2.add_neighbor(tile1)
        # Glue octagon vertices together
        edge_tiles = []
        for start in range(glue_start, len(self.tiles), columns_final):
            edge_tiles.append(self.tiles[start])
            edge_tiles.append(self.tiles[start+columns_final-1])
        for tile1 in edge_tiles:
            for tile2 in edge_tiles:
                if tile1==tile2: continue
                tile1.add_neighbor(tile2)
                tile2.add_neighbor(tile1)

    def tile_at(self, x, y):
        for tile in self.tiles:
            tri_coords = [list(coord) for coord in tile.coordinates]
            # Condition for triangle inside
            if not round_hundredths(area_triangle(tri_coords)) < round_hundredths(area_triangle(tri_coords[:2]+[[x, y]]) + area_triangle(tri_coords[1:]+[[x, y]]) + area_triangle(tri_coords[::2]+[[x, y]])):
                return tile


if __name__=="__main__":
    start = time.time()
    board = MSGenusGBoard([False for i in range(80000)], 2)
    end = time.time()
    print("Time to build 80000 tile board: %f seconds" % (end-start))