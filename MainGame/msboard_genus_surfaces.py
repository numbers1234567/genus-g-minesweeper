import msboard
from math import sin, cos, pi, sqrt, ceil
import numpy as np

def rotate2d(vec, theta):
    return np.dot([[cos(theta), -sin(theta)],
                   [sin(theta), cos(theta)]], vec)

def area_triangle(coords):
    return 0.5*np.linalg.det([list(coords[0])+[1],
                              list(coords[1])+[1],
                              list(coords[2])+[1]])

def round_hundredths(num):
    return round(num*100)/100

class MSGenusG(msboard.MSTile):
    def __init__(self, hasmine, id_, revealed=False, flagged=False, neighbors=[]):
        super().__init__(hasmine, id_, revealed=revealed, flagged=flagged, neighbors=neighbors)

    """
    Takes the genus of the surface and returns out the coordinates of this tile when
    the surface is mapped to a regular polygon
    """
    def get_triangle_coordinates(self, genus):
        numsides = genus*4
        large_angle = (pi-2*pi/numsides)/2
        triangle_height = sin(large_angle)
        triangle_width = 2*cos(large_angle)
        # (sector, row, column)
        row = int(sqrt(self.id/numsides))
        sector = int((self.id-numsides*(row**2))/numsides)
        column = (self.id-numsides*(row**2))%(2*row+1)
        # Base for the coordinates
        coordinates_base = np.array([[0, 0], 
                                    [cos(large_angle), sin(large_angle)], 
                                    [-cos(large_angle), sin(large_angle)]])
        if column%2==1: coordinates_base = np.array([0, sin(large_angle)]) - coordinates_base
        # Shift to row and column
        coordinates_base += np.array([(column-row)*cos(large_angle), row*sin(large_angle)])
        # Rotate to sector
        rotation_a = -2*pi*sector/numsides
        return np.array([np.array([round_hundredths(dim) for dim in rotate2d(vec, rotation_a)]) 
                                                            for vec in coordinates_base])


class MSGenusGBoard(msboard.MSBoard):
    def __init__(self, mine_locs, genus):
        self.genus = genus
        super().__init__(mine_locs, MSGenusG)

    def neighbor_criteria(self, tile1, tile2):
        for coord1 in tile1.get_triangle_coordinates(self.genus):
            for coord2 in tile2.get_triangle_coordinates(self.genus):
                if False not in list(coord1==coord2): return True

    def tile_at(self, x, y):
        for tile in self.tiles:
            tri_coords = [list(coord) for coord in tile.get_triangle_coordinates(self.genus)]
            # Condition for triangle inside
            if round_hundredths(area_triangle(tri_coords)) < round_hundredths(area_triangle(tri_coords[:2]+[x, y]) + area_triangle(tri_coords[1:]+[x, y]) + area_triangle(tri_coords[::2]+[x, y])):
               return tile