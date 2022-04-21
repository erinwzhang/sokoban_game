# 6.009 Lab 2: Snekoban

import json
from operator import truediv
import this
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    game = {
        'wall': set(),
        'target': set(),
        'computer': set(),
        'player': set(),
        'width': len(level_description[0]),
        'height': len(level_description)
    }
    for i in range(len(level_description)):
        for j in range(len(level_description[0])):
            for object in level_description[i][j]:
                game[object].add((i, j)) # add coordinate to object's set
    return game


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """
    if game['target'] == game['computer'] and game['target']: # need to check if there are any targets
        return True
    return False


def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    cpy = copy_game(game)
    player_loc = list(cpy['player'])[0] # only one player, will be first tup
    dir = direction_vector[direction]
    target_loc = (player_loc[0] + dir[0], player_loc[1] + dir[1])
    if target_loc in cpy['computer']:
        after_target = (target_loc[0] + dir[0], target_loc[1] + dir[1]) # space after target move
        if after_target not in cpy['computer'] and after_target not in cpy['wall']:
            cpy['player'].add(target_loc)
            cpy['player'].remove(player_loc)
            cpy['computer'].add(after_target)
            cpy['computer'].remove(target_loc)
    elif target_loc not in cpy['wall']: # path is clear
        cpy['player'].add(target_loc)
        cpy['player'].remove(player_loc)
    return cpy


def copy_game(game):
    """
    Make a deep copy of the game
    """
    cpy = {}
    for object in game.keys():
        if object != 'width' and object != 'height':
            cpy[object] = game[object].copy()
    cpy['width'] = game['width']
    cpy['height'] = game['height']
    return cpy


def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    width, height = game['width'], game['height']
    output = []
    # create dimensionally correct empty lists
    for i in range(height):
        row = []
        for j in range(width):
            row.append([])
        output.append(row)
    # load values
    for object in game.keys():
        if object != 'width' and object != 'height':
            for coords in game[object]:
                output[coords[0]][coords[1]].append(object)
    return output


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    visited = set()
    agenda = []
    visited.add((frozenset(game['player']), frozenset(game['computer']))) # tuple of player and computer locs
    agenda.append((game, [])) # game states and paths

    # check until a path found or no more paths possible
    while agenda:
        current_game = agenda.pop(0)
        if victory_check(current_game[0]):
            return current_game[1] # second entry is path
        for direction in direction_vector.keys(): # possible directions
            new = step_game(current_game[0], direction) # game produced by step
            state = (frozenset(new['player']), frozenset(new['computer'])) # somehow freezing other stuff???
            if state not in visited:
                visited.add(state)
                # if not computer_cornered(new):
                agenda.append([new, current_game[1] + [direction]]) # add to path
    return None

# def computer_cornered(game):
#     for computer_coord in game['computer']:
#         count = 0
#         for direction_coord in direction_vector.values():
#             if (computer_coord[0] + direction_coord[0], computer_coord[1] + direction_coord[1]) in game['wall']:
#                 count += 1
#         if count == 3:
#             return True
#     return False


if __name__ == "__main__":
    pass
    # bar = [
    #     [["wall"], ["wall"], ["wall"], ["wall"], ["wall"]], 
    #     [["wall"], [], ["player"], [], ["wall"]], 
    #     [["wall"], [], [], [], ["wall"]], 
    #     [["wall"], [], [], [], ["wall"]], 
    #     [["wall"], ["wall"], ["wall"], ["wall"], ["wall"]]]
    # foo = [
    #     [[], ['wall'], ['computer']],
    #     [['target', 'player'], ['computer'], ['target']],
    # ]
    # game = new_game(foo)
    # dump = dump_game(game)
    # new = step_game(game, 'up')
    # new_dump = dump_game(new)
    # # print(victory_check(new))
    # # print(game)
    # print(dump)
    # # print(game)
    # # print(new)
    # print(new_dump)
    # # print(output)