# revealed : 0, unknown : 1, flagged : 2
import sys
sys.path.append("..")
from board_definitions import *
from Solver.SolverCSPGenus import *
from random import randint, shuffle

"""
gen_graph_solver_data
Generate graph data for solver
Returns a tuple (edges, tile states), where edges is a set and tile states is a dictionary
Each element of edges is an tuple of form
    (tile1 id, tile2 id)

Each item of tile_states is of form tile id : tile label,
 where tile_label is in form (tile type, # of mines)

This function essentially recurses itself to access degree n neighbors.
I believe the time complexity is something like O(d * n**2) where n is the number of tiles and d is the search degree.
"""
def partial_gen_graph_solver_data(msboard, target_id, ignore_tiles=None, degree=8):
    if degree==0: return (set([]), {}) # Base case
    if ignore_tiles==None:
        ignore_tiles = [100000 for tile in msboard.tiles]
    elif ignore_tiles[target_id] < degree: return (set([]), {}) # Useless search
    ignore_tiles[target_id] = degree
    target_tile = msboard.tiles[target_id]
    neighbors_important = [neighbor for neighbor in target_tile.get_neighbors() if edge_is_helpful(msboard, target_id, neighbor.id)]
    edges = set([(target_id, neighbor.id) for neighbor in neighbors_important])
    tile_states = {neighbor.id : (tiletype(neighbor), (-1 if tiletype(neighbor) != 0 else neighbor.get_num_adjacent_mines())) for neighbor in neighbors_important}

    for neighbor in neighbors_important:
        neighbor_edges, neighbor_states = gen_graph_solver_data(msboard, neighbor.id, ignore_tiles=ignore_tiles, degree=degree-1)
        edges.update(neighbor_edges)
        tile_states = {**tile_states, **neighbor_states}
    
    return (edges, tile_states)


"""
Returns entire board as described in partial_gen_graph_solver_data if unknown==True
Else, simply returns whether each tile has a mine (like [1,0,0,1,1,0])
"""
def whole_gen_graph_solver_data(msboard, unknown=True):
    edges = set([])
    tile_states = {}
    for tile in msboard.tiles:
        # Tile state
        tile_states[tile.id] = (tiletype(tile), (-1 if tiletype(tile) != 0 else tile.get_num_adjacent_mines()))
        if not unknown: tile_states[tile.id] = true_tiletype(tile)
        # Edges
        neighbors_important = [neighbor for neighbor in tile.get_neighbors() if edge_is_helpful(msboard, tile.id, neighbor.id)]
        new_edges = set([(tile.id, neighbor.id) for neighbor in neighbors_important])
        edges.update(new_edges)

    if unknown: return (edges, tile_states)
    else: return [tile_states[i] for i in range(len(msboard.tiles))]

"""
Gives the tiletype represented as an int
"""
def tiletype(tile):
    if tile.revealed: return 0
    if tile.flagged: return 2
    return 1
def true_tiletype(tile):
    return tile.hasmine

"""
Some basic criteria to determine if a given edge actually influences calculation
"""
def edge_is_helpful(msboard, target_id, other_id): 
    # Helper function to determine if a candidate edge actually helps
    # (target, other) : (revealed, unknown), (revealed, flagged), (unknown, releaved), (flagged, revealed)
    true_cases = [(0, 1), (0, 2), (1, 0), (2, 0)]
    target_type = tiletype(msboard.tiles[target_id])
    other_type = tiletype(msboard.tiles[other_id])
    return (target_type, other_type) in true_cases

"""
Train generator for gnn data.
Saves multiple concurrent boards at different stages of solving
Parameters:
 * num_concurrent - number of conccurent boards to save
 * geni - a list of possible genuses
 * possible_num_tiles - a list of lists, where each list contains the possible number of tiles
Yields:
 * A list of tuples [(X, Y), etc], each element for each concurrent board
   * X is a tuple of form (edges, tile states) given by whole_gen_graph_solver_data
   * Y is a tuple giving the true tile states.
"""
def train_generator(num_concurrent=10, geni=[2], possible_num_tiles=[[32, 72, 128, 200, 288, 392, 512, 648, 800, 968]]):
    genus_vals = [genus for genus in geni]
    num_tiles = [[num for num in genus] for genus in possible_num_tiles]

    board_types = [genus_generate_compatible_class(genus)[0] for genus in genus_vals]

    boards = []
    solvers = []
    # Set up initial state
    for i in range(num_concurrent):
        #print(i)
        index = randint(0, len(board_types)-1)
        # Set up board
        n = num_tiles[index][randint(0, len(num_tiles[index])-1)]
        first_click = randint(0, n-1)
        mine_locs = load_random_board(board_types[index], n, randint(n//10, n//4), firstclick_id=first_click)
        boards.append(board_types[index](mine_locs))
        boards[i].on_click_reveal(boards[i].tiles[first_click])
        
        # Set up solver
        solvers.append(-1)
        #update_solver(solvers[i], boards[i])

        # Further randomize the board state (might do something other than solve, since that's expensive)
        for _ in range(randint(0, 4)): boards[i], solvers[i] = board_step(boards[i], solvers[i], board_types, num_tiles)

    while True:
        # Yield all graphs for training
        ret = [(whole_gen_graph_solver_data(board), whole_gen_graph_solver_data(board, unknown=False)) for board in boards]
        shuffle(ret)
        # Single solve step (might do something other than solve, since that's expensive)
        for i in range(len(boards)):
            boards[i], solvers[i] = board_step(boards[i], solvers[i], board_types, num_tiles)
        yield ret

"""
Update solver to correspond with board
"""
def update_solver(solver, board):
    new_labels = []
    for tile in board.tiles:
        if tile.flagged: new_labels.append(-1)
        elif not tile.revealed: new_labels.append(-2)
        else: new_labels.append(tile.get_num_adjacent_mines())

    solver.update(new_labels)

def board_step_reveal(tile):
    # Return whether or not to open the tile in board_step
    if tile.revealed: return 0
    if tile.flagged: return 1
    if tile.hasmine:
        if True in [neighbor.revealed for neighbor in tile.get_neighbors()]: return 1
        return 2
    if True in [neighbor.revealed for neighbor in tile.get_neighbors()]: return 0
    return 2


"""
Single solve step on board and solver.
Returns (msboard, solver) if another step is needed
Returns a new (msboard, solver) if no new step is needed
"""
def board_step(msboard, solver, board_types, num_tiles):
    #solver.predict()
    pred = [board_step_reveal(tile) for tile in msboard.tiles]

    # Update board
    for i in range(len(pred)):
        if pred[i] == 0: msboard.on_click_reveal(msboard.tiles[i])
        elif pred[i] == 1 and not msboard.tiles[i].flagged: msboard.on_click_toggleflag(msboard.tiles[i])
    if 2 not in pred: # A new msboard and solver is needed
        index = randint(0, len(board_types)-1)
        n = num_tiles[index][randint(0, len(num_tiles[index])-1)]
        first_click = randint(0, n-1)
        mine_locs = load_random_board(board_types[index], n, randint(n//10, n//4), firstclick_id=first_click)
        msboard = board_types[index](mine_locs)
        msboard.on_click_reveal(msboard.tiles[first_click])
        #solver = CSPSolverGenus(msboard.genus, [2 for i in range(n)])
    # Update solver
    #update_solver(solver, msboard)

    return (msboard, solver)