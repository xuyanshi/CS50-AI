"""
Tic Tac Toe Player
"""

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
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x += 1
            elif board[i][j] == O:
                o += 1
    return O if o < x else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    score = utility(board)
    if score == 1:
        return X
    elif score == -1:
        return O


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    score = utility(board)
    return score == 1 or score == -1


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
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
    raise NotImplementedError
