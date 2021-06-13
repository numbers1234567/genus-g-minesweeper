from MainGame.msboard import MSTile
from random import randint

def load_random_board(board_type, num_tiles, num_mines, firstclick_id=None, tile_class=MSTile):
    empty_board = board_type([False for i in range(num_tiles)])
    # Now that we have an empty board, generate mines at certain ids
    id_contains_mine = [False for i in range(num_tiles)]
    for i in range(num_mines):
        while True:
            index = randint(0, len(id_contains_mine)-1)
            if (not id_contains_mine[index]) and (not empty_board.neighbor_criteria(empty_board.tiles[index], empty_board.tiles[firstclick_id])):
                id_contains_mine[index] = True
                break
    
    return id_contains_mine