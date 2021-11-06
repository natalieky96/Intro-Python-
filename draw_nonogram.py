
WHITE = 0
BLACK = 1
UNKNOWN = -1


WHITE_BLANK_REP = 0
BLACK_BLANK_REP = 1
WHITE_BLANK = "_"
BLACK_BLANK = "X"
UNKNOWN_BLANK = "?"
CHR_SEPARATOR = " "

import math

NO_SOLUTIONS = 0


def is_block_ok(row, one_block, idx):
    """Check if the block may appear in the current row
    :param row: The current row
    :param one_block: The block we want to check
    :param idx: The index in the row
    :return: True if it possible, otherwise False, and the index of the end
    of the block
    """
    counter = 0
    while idx < len(row):
        if one_block == 1 and row[idx] in [BLACK, UNKNOWN]:
            if idx == 0 and row[idx+1] in [WHITE, UNKNOWN]:
                return True
            if idx == (len(row)-1):
                if row[idx-1] in [WHITE, UNKNOWN]:
                    return True
                else:
                    break
            if row[idx+1] in [WHITE, UNKNOWN] and row[idx-1] in\
                    [WHITE, UNKNOWN]:
                return True
        if row[idx] in [BLACK, UNKNOWN]:
            counter += 1
            if idx+1 == len(row):
                break
        if row[idx] == WHITE and row[idx - 1] in [BLACK, UNKNOWN] and idx != 0:
            break
        idx += 1
    if counter == one_block:
        return True

    return False


def valid_row(row, block):
    """Checks if the constraints are valid to the row
    :param row: The current row
    :param block: The size and the blocks we want to fill with
    :return: True if it is valid, otherwise False
    """
    num_black = row.count(BLACK)
    num_unknown = row.count(UNKNOWN)
    num_white = row.count(WHITE)
    # The number of all black blocks
    sum_black = sum(block)
    # If there isn't enough black space
    if num_black + num_unknown < sum_black:
        return False
    # Check if there is enough space between each block
    if num_white + num_unknown < (len(block) - 1):
        return False
    if (len(block) - 1) + sum_black > len(row):
        return False
    if row.count(UNKNOWN) == 0 and sum_black != num_black:
        return False
    if BLACK in row:
        idx = row.index(BLACK)
    for b in block:
        possible = is_block_ok(row, b, idx)
        # Find the first place BLACK appears after the previous block
        if BLACK in row[idx+b:]:
            idx = row.index(BLACK, idx + b)
        if not possible:
            return False

    return True


def help_get_row_variations(row, blocks, lst):
    """Get a row, its constraints(blocks) and a list and add to the list
    all the options of coloring the row.
    :param row: Our current row
    :param blocks: The constraints(The blocks)
    :param lst: An empty list, where we add the valid option.
    :return: The list with the coloring options.
    """
    if row.count(UNKNOWN) == 0:
        if valid_row(row, blocks):
            lst.append(row.copy())
        return
    # Save the original value of the index, find the first place UNKNOWN IS
    # FOUND

    replaced_index = row.index(UNKNOWN)
    # Try with while
    help_get_row_variations(row[:replaced_index] + [WHITE] + row[
                                                             replaced_index
                                                             + 1:], blocks,
                            lst)

    # Try with black
    help_get_row_variations(
        row[:replaced_index] + [BLACK] + row[replaced_index + 1:],
                            blocks, lst)


def get_row_variations(row, blocks):
    """Get a row, its constraints(blocks) and return all the options of
     coloring the row.
    :param row: The current row.
    :param blocks: The constraints(The blocks)
    :return: The list with the coloring options.
    """
    variations_lst = []
    help_get_row_variations(row, blocks, variations_lst)
    return variations_lst


def get_intersection_row(rows):
    """Get list of lists and return a final list with the common combination,
    if the square doesn't have a common value make it UNKNOWN
    :param rows: A list of lists(combinations)
    :return: A list of the common combination
    """
    # Add to the return list all the same values, otherwise UNKNOWN
    out_lst = []
    if len(rows) == 0:
        return out_lst
    first_row = rows[0]
    for idx in range(len(first_row)):
        for idx2 in range(len(rows)):
            if first_row[idx] != rows[idx2][idx]:
                out_lst.append(UNKNOWN)
                break
            if idx2 == len(rows) - 1:
                out_lst.append(first_row[idx])
    return out_lst


def column_to_row(board, num_column):
    """Get a board and it's index and make it to a row
    :param board: Our board
    :param num_column: the number of the column we want to change
    :return: A list of the specific column as a row
    """
    out_lst = []  # THe list we want to return
    for i in range(len(board)):
        out_lst.append(board[i][num_column])
    return out_lst


def row_to_column(board, num_column, row):
    """Get a row  and make it to a column in num_column index
    :param board: Our board
    :param num_column: the number of the column we want to insert the row
    :param row: The row we want to insert to the board
    :return: A new board with the inserted row
    """
    for i in range(len(board)):
        board[i][num_column] = row[i]
    return board


def valid_row_board(board, const):
    """Get a board and color it by the constraints rows
    :param board: The current board
    :param const: The constraints of the rows
    :return: A new board with the final const changes
    """
    for i in range(len(board)):
        # Get all the possible variations
        variation_lst = get_row_variations(board[i], const[i])
        if len(variation_lst) == 0:
            continue
        common_variation = get_intersection_row(variation_lst)
        board[i] = common_variation
    return board


def valid_column_board(board, const):
    """Get a board and color it by the constraints columns
    :param board: The current board
    :param const: The constraints of the columns
    :return: The current board with the final const changes
    """
    for i in range(len(board[0])):
        # Make it to a row
        current_column = column_to_row(board, i)
        # Get all the possible variations
        variation_lst = get_row_variations(current_column, const[i])
        if len(variation_lst) == 0:
            continue
        common_variation = get_intersection_row(variation_lst)
        # insert the new column to the board
        row_to_column(board, i, common_variation)

    return board


def solve_easy_nonogram(constraints):
    """Get constraints and return a solved game.
    :param constraints: A list of list of constraints
    :return: A solved game
    """
    board = []  # The board we build
    # if the constraints are empty return None
    if len(constraints) == 0:
        return board
    row_const = constraints[0]
    column_const = constraints[1]
    # If one of the constraints are empty and the other isn't it isn't possible
    # and return None
    if len(row_const) == 0 and len(column_const) != 0:
        return None
    if len(row_const) != 0 and len(column_const) == 0:
        return None
    # if 2 of the constraints are empty the board is one white square
    if len(row_const) == 0 and len(column_const) == 0:
        board = [[WHITE]]
        return board
    # Building an empty board
    for i in range(len(constraints[0])):
        board.append([])
        for j in range(len(constraints[1])):
            board[i].extend([UNKNOWN])
    # Save a the board to equal it to the previous board
    saved_board = []
    # Run until we can do more changes
    while saved_board != board:
        saved_board = board.copy()
        board = valid_row_board(board, row_const)
        board = valid_column_board(board, column_const)

    return board


def solve_nonogram(constraints):
    """Get constraints of the nonogram board and return a list of the
    solutions.
    :param constraints: constraints of the nonogram board
    :return: A list of the solutions.
    """
    list_solutions = solve_easy_nonogram(constraints)
    # If there isn't solution return an empty list
    if list_solutions is None:
        return []
    else:
        return [list_solutions]


def count_row_variations(length, blocks):
    """Get length of a row and lists of constraints and return the number of
     possibilites of coloring.
    :param length: The length of the row
    :param blocks: list of constraints
    :return: The number of possiblities to color the row according the
    constraints.
    """
    # The formula of combiniatora is length of the row - numbers of total
    # black in factorial / number of blocks in factorial * (length of row -
    # num black + 1 - number of blocks) in factorial
    num_black = sum(blocks)
    num_blocks = len(blocks)
    if length - num_black + 1 <= 0:
        return NO_SOLUTIONS
    if length - num_black + 1 - num_blocks <= 0:
        return NO_SOLUTIONS
    variations = math.factorial(length - num_black + 1) / (math.factorial(
        num_blocks) * math.factorial(length - num_black + 1 - num_blocks))

    return variations


def print_board(board):
    """
    This function prints the input board game to the screen.
    :param board: The matrix that represents the game board.
    :return: None
    """
    if board is None:
        return None
    rep_str = ""
    for row in board:
        for blank in row:
            if blank == WHITE_BLANK_REP:
                rep_str += WHITE_BLANK
            elif blank == BLACK_BLANK_REP:
                rep_str += BLACK_BLANK
            else:
                rep_str += UNKNOWN_BLANK
            rep_str += CHR_SEPARATOR
        rep_str += "\n"
    print(rep_str)


constraints_cat = [
    [[3], [1], [1], [3, 1], [1, 4, 1], [2, 6], [4, 3], [1, 2], [1, 1], [1, 1],
     [2, 2]], [[2], [3, 1], [5], [3], [3], [3], [1, 5, 1], [1, 6], [7]]]

nonogram_cat = [[0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 1, 1, 0, 1],
                [0, 1, 0, 1, 1, 1, 1, 0, 1], [1, 1, 0, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 1, 1, 1], [0, 0, 1, 0, 0, 0, 1, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0, 0, 1, 0],
                [0, 1, 1, 0, 0, 0, 1, 1, 0]]

hannukia = [[
    [1, 1, 1, 1, 2, 1, 1, 1, 1],
    [2],
    [1, 1, 1, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 6, 1, 1, 1],
    [1, 1, 1, 2, 1, 1, 1],
    [1, 1, 10, 1, 1],
    [1, 1, 2, 1, 1],
    [1, 14, 1],
    [1, 2, 1],
    [18],
    [2],
    [1, 2],
    [5, 2, 1],
    [3, 4, 5],
    [1, 6, 3],
    [8, 1],
],
    [
        [1, 8, 1],
        [1, 2],
        [1, 6, 1, 4],
        [1, 1, 2],
        [1, 4, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 2, 1, 1, 1, 2],
        [1, 1, 1, 1, 3],
        [16],
        [16],
        [1, 1, 1, 1, 3],
        [1, 2, 1, 1, 1, 2],
        [1, 1, 1, 1],
        [1, 4, 1, 1, 1],
        [1, 1, 2],
        [1, 6, 1, 4],
        [1, 2],
        [1, 8, 1],
    ]]

row = [-1, -1,-1]
hello = [2]
# row = [-1, -1,-1,-1]
# hello = [2]
# row = [-1, -1,-1,-1,-1,-1]
# hello = [1, 2, 1]
#[1, 0, 1, 0,1,1,1,1,1,1,1,1,1,1, 0, 1, 0 ,1], [1, 1, 10, 1,

const5 = [[[3],[],[]],[[1],[1],[1]]]
#nonogram= solve_easy_nonogram(constraints_cat)
#print_board(nonogram)
#print(valid_column_board([[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
#                              -1]],
#                         [16]))

#print_board(solve_easy_nonogram([[[1],[1],[5],[1],[1]], [[1],[1],[5],[1],
#                                                        [1]]]))

yolo =  [[
    [2, 18],
    [1, 20],
    [23],
    [23],
    [24],
    [25],
    [25],
    [19, 4],
    [14, 3, 4],
    [13, 6, 3],
    [11, 8, 3],
    [12, 2, 2, 3],
    [7, 2, 3],
    [5, 3, 3, 3],
    [4, 1, 1, 1, 1, 1, 1, 3],
    [4, 1, 3, 3, 1, 3],
    [4, 1, 2, 2, 1, 1, 1],
    [1, 2, 2, 1, 1],
    [1, 2, 4, 1, 3, 1],
    [1, 1 ,1, 2],
    [1, 1, 1, 1],
    [2, 13, 3],
    [3, 1, 3, 1],
    [1, 3, 12, 1, 1],
    [5, 10, 2, 1],
    [6, 8, 2, 1],
    [7, 5, 2, 1],
    [3, 3],
    [3, 3],
    [15]
],
    [
        [17, 4],
        [15, 2, 3],
        [19, 5],
        [1, 19, 5],
        [13, 4],
        [13, 2],
        [13, 3, 1, 2, 1],
        [12, 1, 1, 3, 1, 1],
        [12, 4, 1, 1, 2, 3],
        [12, 1, 2, 1, 1, 3, 2],
        [12, 2, 1, 4, 2],
        [10, 1, 1, 4, 1],
        [10, 1, 1, 4, 1],
        [9, 3, 1, 4, 1],
        [8, 3, 1, 1, 4, 1],
        [11, 2, 1, 3, 2],
        [11, 2, 1, 3, 2],
        [11, 1, 2, 1, 4, 3],
        [8, 2, 4, 1, 3, 2, 1],
        [7, 3, 1, 1, 2, 3, 1],
        [7, 2, 3, 2, 1],
        [9, 6],
        [18, 1],
        [15, 3],
        [16, 4]
    ]]

more_than_1_solution = [[[1,3], [], [1], [1, 1], [1, 2]],[[1, 1], [1], [1], [1, 3], [1, 1]]]

import timeit

start = timeit.default_timer()

print_board(solve_easy_nonogram(hannukia))
n = timeit.default_timer()
print(n-start)
