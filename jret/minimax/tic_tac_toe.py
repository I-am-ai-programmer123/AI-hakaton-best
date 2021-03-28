import numpy as np
import constants as const
from minimax import minimax, minimax_alpha_beta, minimax_alpha_beta_memo


def antidiag(matrix):
    n = matrix.shape[0]

    return np.array([matrix[i, n - 1 - i] for i in range(n)])


def game_state(board):

    if np.any(np.all(board == const.PLAYER_X, 0)
              | np.all(board == const.PLAYER_X, 1)
              | np.all(np.diag(board) == const.PLAYER_X)
              | np.all(antidiag(board) == const.PLAYER_X)):

        return True, const.PLAYER_X

    elif np.any(np.all(board == const.PLAYER_O, 0)
                | np.all(board == const.PLAYER_O, 1)
                | np.all(np.diag(board) == const.PLAYER_O)
                | np.all(antidiag(board) == const.PLAYER_O)):

        return True, const.PLAYER_O

    elif not np.any(board == const.PLAYER_NEUTRAL):
        return True, const.PLAYER_NEUTRAL

    return False, None


def heuristic_win_moves(board, player):

    is_game_over, winner = game_state(board)
    if is_game_over:
        return np.nan if winner == const.PLAYER_NEUTRAL else winner * np.inf

    heur_val = 0

    heur_val += np.sum(np.any(board == player, 0) & ~np.any(board == -player, 0))
    heur_val += np.sum(np.any(board == player, 1) & ~np.any(board == -player, 1))

    heur_val += np.sum(np.any(np.diag(board) == player)
                       & ~np.any(np.diag(board) == -player))

    heur_val += np.sum(np.any(antidiag(board) == player)
                       & ~np.any(antidiag(board) == -player))

    return player * heur_val


def heuristic_tile_weights(board, player):

    is_game_over, winner = game_state(board)
    if is_game_over:
        return np.nan if winner == const.PLAYER_NEUTRAL else winner * np.inf

    tile_weights = np.array([[2, 1, 2],
                             [1, 3, 1],
                             [2, 1, 2]])

    return np.sum(tile_weights * board)


def available_moves(node, player_turn):
    free_indexes = list(zip(*np.where(node == const.PLAYER_NEUTRAL)))

    return free_indexes


def make_move(board, move, player):
    if board[move[0], move[1]] != const.PLAYER_NEUTRAL:
        raise ValueError("Invalid move!")

    board[move[0], move[1]] = player

    return board


def ai_move(board, player, algoritm="minimax", heur="win_moves"):

    if heur == "win_moves":
        heuristic = heuristic_win_moves
    elif heur == "tile_weights":
        heuristic = heuristic_tile_weights
    else:
        raise ValueError("Invalid Heuristic!")

    if algoritm == "minimax":
        return minimax(board,
                       heuristic,
                       available_moves,
                       const.MINIMAX_MAX_DEPTH,
                       player,
                       make_move)[1]

    elif algoritm == "alpha-beta":
        return minimax_alpha_beta(board, 
                                  heuristic,
                                  available_moves,
                                  const.MINIMAX_MAX_DEPTH,
                                  player,
                                  make_move)[1]

    elif algoritm == "alpha-beta-memo":
        return minimax_alpha_beta_memo(board,
                                       heuristic,
                                       available_moves,
                                       const.MINIMAX_MAX_DEPTH,
                                       player,
                                       make_move)[1]
