import numpy as np
import random


def minimax(node, heuristic, available_moves, depth, player, make_move):
    """ MiniMax algorithm """
    heur_val = heuristic(node, player)

    if depth <= 0 or not np.isfinite(heur_val):
        return 0 if np.isnan(heur_val) else heur_val, None

    possible_moves = available_moves(node, player)
    best_move = random.choice(possible_moves)

    if player > 0:
        heur_val = -np.inf
        for new_move in possible_moves:
            child_node = np.copy(node)
            child_node = make_move(child_node, new_move, player)
            new_heur_val, _ = minimax(child_node, heuristic,
                                      available_moves, depth - 1,
                                      -player, make_move)

            if new_heur_val > heur_val:
                heur_val = new_heur_val
                best_move = new_move

            elif new_heur_val == heur_val:
                best_move = random.choice([best_move, new_move])

    else:
        heur_val = np.inf
        for new_move in possible_moves:
            child_node = np.copy(node)
            child_node = make_move(child_node, new_move, player)
            new_heur_val, _ = minimax(child_node, heuristic,
                                      available_moves, depth - 1,
                                      -player, make_move)

            if new_heur_val < heur_val:
                heur_val = new_heur_val
                best_move = new_move

            elif new_heur_val == heur_val:
                best_move = random.choice([best_move, new_move])

    return heur_val, best_move


def minimax_alpha_beta(node, heuristic, available_moves, depth,
                       player, make_move,  alpha=-np.inf, beta=np.inf):
    """ MiniMax algorithm with alpha-beta purning"""

    heur_val = heuristic(node, player)

    if depth <= 0 or not np.isfinite(heur_val):
        return 0 if np.isnan(heur_val) else heur_val, None

    possible_moves = available_moves(node, player)
    best_move = random.choice(possible_moves)

    if player > 0:
        heur_val = -np.inf
        for new_move in possible_moves:
            child_node = np.copy(node)
            child_node = make_move(child_node, new_move, player)
            new_heur_val, _ = minimax_alpha_beta(child_node, heuristic,
                                                 available_moves, depth - 1,
                                                 -player, make_move, alpha, beta)

            if new_heur_val > heur_val:
                heur_val = new_heur_val
                best_move = new_move

            alpha = max(alpha, heur_val)
            if alpha >= beta:
                break

    else:
        heur_val = np.inf
        for new_move in possible_moves:
            child_node = np.copy(node)
            child_node = make_move(child_node, new_move, player)
            new_heur_val, _ = minimax_alpha_beta(child_node, heuristic,
                                                 available_moves, depth - 1,
                                                 -player, make_move, alpha, beta)

            if new_heur_val < heur_val:
                heur_val = new_heur_val
                best_move = new_move

            beta = min(beta, heur_val)
            if beta <= alpha:
                break

    return heur_val, best_move


def minimax_alpha_beta_memo(node, heuristic, available_moves, depth,
                            player, make_move, alpha=-np.inf, beta=np.inf,
                            memo={}):
    """ MiniMax algorithm with alpha-beta purning and memoization of game states"""

    if (node.tobytes(), player) in memo:
        return memo[(node.tobytes(), player)]

    heur_val = heuristic(node, player)

    if depth <= 0 or not np.isfinite(heur_val):
        return 0 if np.isnan(heur_val) else heur_val, None

    possible_moves = available_moves(node, player)
    best_move = random.choice(possible_moves)

    if player > 0:
        heur_val = -np.inf
        for new_move in possible_moves:
            child_node = np.copy(node)
            child_node = make_move(child_node, new_move, player)
            new_heur_val, _ = minimax_alpha_beta(child_node, heuristic,
                                                 available_moves, depth - 1,
                                                 -player, make_move, alpha, beta)

            if new_heur_val > heur_val:
                heur_val = new_heur_val
                best_move = new_move

            alpha = max(alpha, heur_val)
            if alpha >= beta:
                break

    else:
        heur_val = np.inf
        for new_move in possible_moves:
            child_node = np.copy(node)
            child_node = make_move(child_node, new_move, player)
            new_heur_val, _ = minimax_alpha_beta(child_node, heuristic,
                                                 available_moves, depth - 1,
                                                 -player, make_move, alpha, beta)

            if new_heur_val < heur_val:
                heur_val = new_heur_val
                best_move = new_move

            beta = min(beta, heur_val)
            if beta <= alpha:
                break

    memo[(node.tobytes(), player)] = (heur_val, best_move)

    return heur_val, best_move
