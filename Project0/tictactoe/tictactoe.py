"""
Tic Tac Toe Player
"""

import itertools
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = o = 0
    for i, j in itertools.product(range(3), range(3)):
        if board[i][j] == X:
            x += 1
        elif board[i][j] == O:
            o += 1
    return O if o < x else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()
    for i, j in itertools.product(range(3), range(3)):
        if board[i][j] is None:
            actions_set.add((i, j))

    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not None:
        raise ValueError("action is not a valid action for the board")
    now_player = player(board)
    new_board = []
    for i, j in itertools.product(range(3), range(3)):
        new_board[i][j] = board[i][j]
    new_board[action[0]][action[1]] = now_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    score = utility(board)
    if score == 1:
        return X
    elif score == -1:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    score = utility(board)
    return score in [1, -1]


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # I make judgements here. But it should be in result() function.
    # horizontal
    for i in range(3):
        x = o = 0
        for j in range(3):
            if board[i][j] == X:
                x += 1
            elif board[i][j] == O:
                o += 1
        if x == 3:
            return 1
        elif o == 3:
            return -1

    # vertical
    for j in range(3):
        x = o = 0
        for i in range(3):
            if board[i][j] == X:
                x += 1
            elif board[i][j] == O:
                o += 1
        if x == 3:
            return 1
        elif o == 3:
            return -1

    # diagonal: from northwest to southeast
    x = o = 0
    for i in range(3):
        j = i
        if board[i][j] == X:
            x += 1
        elif board[i][j] == O:
            o += 1
    if x == 3:
        return 1
    elif o == 3:
        return -1

    # diagonal: from northeast to southwest
    x = o = 0
    for i in range(3):
        j = 2 - i
        if board[i][j] == X:
            x += 1
        elif board[i][j] == O:
            o += 1
    if x == 3:
        return 1
    elif o == 3:
        return -1

    # otherwise
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    optimal_action = (-1, -1)
    acts = actions(board)
    if player(board) == X:  # X for max

        print(0)
    else:  # O for min

        print(0)

    return optimal_action


# from slides
def max_value(board):
    if terminal(board):
        return utility(board)
    v = -10 ** 10  # -inf, -2 is enough for this problem
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


# from slides
def min_value(board):
    if terminal(board):
        return utility(board)
    v = 10 ** 10  # inf, 2 is enough for this problem
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
