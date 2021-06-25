
from SolverCSP import *
from math import pi, sin, cos, sqrt

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

def get_triangle_coordinates(genus, id_):
    numsides = genus*4
    large_angle = (pi-2*pi/numsides)/2
    triangle_height = sin(large_angle)
    triangle_width = 2*cos(large_angle)
    # (sector, row, column)
    row = int(sqrt(id_/numsides))
    sector = int((id_-numsides*(row**2))/(2*row+1))
    column = (id_-numsides*(row**2))%(2*row+1)
    # Base for the coordinates
    coordinates_base = [[0, 0], 
                        [cos(large_angle), sin(large_angle)], 
                        [-cos(large_angle), sin(large_angle)]]
    if column%2==1: coordinates_base = [[0, sin(large_angle)], [-cos(large_angle), 0], [cos(large_angle), 0]]
    coordinates_base = [shift_vector(coord, [(column-row)*cos(large_angle), row*sin(large_angle)]) for coord in coordinates_base]
    # Rotate to sector
    rotation_a = -2*pi*sector/numsides
    return [tuple([round_hundredths(dim) for dim in rotate2d(vec, rotation_a)]) for vec in coordinates_base]

class CSPSolverGenus(CSPSolver):
    def __init__(self, genus, tiletypes):
        self.genus = genus
        self.numrows = int(sqrt(len(tiletypes)/(4*genus)))
        super().__init__(tiletypes, n_tiles_total=len(tiletypes))
    
    def neighbor_criteria(self, tile1, tile2):
        for coord1 in get_triangle_coordinates(self.genus, tile1.id):
            for coord2 in get_triangle_coordinates(self.genus, tile2.id):
                #print(coord1)
                #print(coord2)
                #if False not in list(coord1==coord2): return True
                if coord1==coord2: return True
                
    def setup_neighbors(self):
        # Set up coordinates
        times=[]
        tile_coordinates = [get_triangle_coordinates(self.genus, tile.id) for tile in self.tiles]
        
        coords = {}
        # Figure out shared points
        for tile in self.tiles:
            tile_coords = tile_coordinates[tile.id]
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
                """first.append(self.tiles[start+from_].coordinates[0])
                second.append(self.tiles[start+3*columns_final-1-from_].coordinates[0])
                first.append(self.tiles[start+from_+columns_final].coordinates[0])
                second.append(self.tiles[start+4*columns_final-1-from_].coordinates[0])"""
                first.append(tile_coordinates[start+from_][0])
                second.append(tile_coordinates[start+3*columns_final-1-from_][0])
                first.append(tile_coordinates[start+from_+columns_final][0])
                second.append(tile_coordinates[start+4*columns_final-1-from_][0])
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

if __name__=="__main__":
    bruh = CSPSolverGenus(2, [CSPSolverTile.TYPECLOSED for i in range(32)])
    print([tile.id for tile in bruh.tiles[8].neighbors])