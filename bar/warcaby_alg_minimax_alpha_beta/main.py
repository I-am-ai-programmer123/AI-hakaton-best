"""
Author: Bartłomiej Baran
"""
import copy
from board import board
from deepdiff import DeepDiff
from math import inf
from random import choice as ch
from os import system, name


class Node():
    """
    Class representing node objects.
    """
    def __init__(self, parent, board, color):
        """
        Constructor of Node class.

        :param parent: parent node
        :type parent: Node

        :param board: board
        :type board: array

        :param color: color of player
        :type color: string
        """
        self.parent = parent
        self.board = board
        self.children = []
        self.value = self.value_board()
        self.color = color
        self.good = False
        self.last = None

    def value_board(self):
        """
        Function to valuate board.
        """
        if self.board is None:
            return 0
        value = 0
        counter = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                if self.board[y][x] == "B" and y < 5:
                    value += 5
                    counter += 1
                if self.board[y][x] == "B" and y > 4:
                    value += 7
                    counter += 1
                if self.board[y][x] == "W" and y > 4:
                    value += -5
                    counter += 1
                if self.board[y][x] == "W" and y < 5:
                    value += -7
                    counter += 1
                if self.board[y][x] == 'b':
                    value += 10
                    counter += 1
                elif self.board[y][x] == 'w':
                    value += -10
                    counter += 1
        if counter > 0:
            return round(value/counter, 4)
        else:
            return None


def clear():
    """
    Clears console.
    """
    if name == "nt":
        system('cls')
    else:
        system('clear')


def print_board(board):
    """
    Prints board.

    :param board: board
    :type board: array
    """
    for i, line in enumerate(board):
        str1 = ""
        for elem in line:
            str1 += elem
            str1 += " "
        print(8-i, str1)
    print("  A B C D E F G H")


def get_enemy_color(color):
    """
    Returns color of enemy.

    :param color: color of player
    :type color: string
    """
    if color == 'B' or color == 'b':
        return 'W'
    else:
        return "B"


def get_pieces_positions(board, color):
    """
    Finds all pieces positions of passed color.

    :param board: board
    :type board: array

    :param color: color of player
    :type color: string
    """
    pos_arr = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == color or board[row][col] == color.lower():
                pos_arr.append([col, row])
    return pos_arr


def get_possible_beats(board, pos):
    """
    Finds all possible beats of piece.

    :param board: board
    :type board: array

    :param pos: position of piece
    :type pos: tuple
    """
    possible_beats = []
    x = pos[0]
    y = pos[1]
    color = board[y][x]
    enemy_color = get_enemy_color(color)
    for yc in [-1, 1]:
        for xc in [-1, 1]:
            if 8 > x+xc > -1 and 8 > y+yc > -1:  # if move in range
                if board[y+yc][x+xc] == enemy_color or board[y+yc][x+xc] == enemy_color.lower():
                    if color == "W" and yc != 1 and 8 > x+2*xc > -1 and 8 > y+2*yc > -1:
                        try:
                            if board[y+yc*2][x+xc*2] == '-':
                                possible_beats.append(([x, y], [x+xc, y+yc], [x+xc*2, y+yc*2]))
                        except Exception:
                            pass
                    if color == "B" and yc != -1 and 8 > x+2*xc > -1 and 8 > y+2*yc > -1:
                        try:
                            if board[y+yc*2][x+xc*2] == '-':
                                possible_beats.append(([x, y], [x+xc, y+yc], [x+xc*2, y+yc*2]))
                        except Exception:
                            pass
            k = 1
            while True and (color == "w" or color == "b"):
                if 8 > x+k*xc > -1 and 8 > y+k*yc > -1:
                    if board[y+k*yc][x+k*xc] == enemy_color or board[y+k*yc][x+k*xc] == enemy_color.lower():
                        try:
                            if board[y+(k+1)*yc][x+(k+1)*xc] == '-' and 8 > x+(k+1)*xc > -1 and 8 > y+(k+1)*yc > -1:
                                possible_beats.append(([x, y], [x+k*xc, y+k*yc], [x+(k+1)*xc, y+(k+1)*yc]))
                                k += 1
                            else:
                                break
                        except Exception:
                            break
                    if board[y+k*yc][x+k*xc] == color or board[y+k*yc][x+k*xc] == color.upper():
                        break
                    if board[y+k*yc][x+k*xc] == '-':
                        k += 1
                else:
                    break
    return possible_beats


def get_possible_reg_moves(board, pos):
    """
    Finds all possible regular moves of piece.

    :param board: board
    :type board: array

    :param pos: position of piece
    :type pos: tuple
    """
    moves = []
    x = pos[0]
    y = pos[1]
    color = board[y][x]
    for i in [-1, 1]:
        for j in [-1, 1]:
            if x+i > -1 and y+j > -1 and x+i < 8 and y+j < 8:
                if color == "W" and j != 1:
                    if board[y+j][x+i] == '-':
                        moves.append(([x, y], [x+i, y+j]))
                elif color == "B" and j != -1:
                    if board[y+j][x+i] == '-':
                        moves.append(([x, y], [x+i, y+j]))
                elif color == "w" or color == "b":
                    k = 1
                    while True:
                        try:
                            if board[y+k*j][x+k*i] == '-' and x+k*i > -1 and y+k*j > -1 and x+k*i < 8 and y+k*j < 8:
                                moves.append(([x, y], [x+k*i, y+k*j]))
                                k += 1
                            else:
                                break
                        except Exception:
                            break
    return moves


def get_next_possible_moves(parents, color):
    """
    Find and returns all possible moves of player
    of passed color.

    :param parents: list of parent nodes
    :type parents: array

    :param color: color of player to check beat
    :type color: string
    """
    found_beat = False
    for pi, parent in enumerate(parents):
        pieces = get_pieces_positions(copy.deepcopy(parent.board), color)
        found_beat = False
        children = []
        for piece in pieces:
            beats = get_possible_beats(copy.deepcopy(parent.board), piece)
            for i in range(0, len(beats)):
                found_beat = True
                child_board = copy.deepcopy(parent.board)
                if child_board[beats[i][0][1]][beats[i][0][0]] == color.lower():
                    child_board[beats[i][2][1]][beats[i][2][0]] = color.lower()
                else:
                    child_board[beats[i][2][1]][beats[i][2][0]] = color
                child_board[beats[i][0][1]][beats[i][0][0]] = "-"
                child_board[beats[i][1][1]][beats[i][1][0]] = "-"
                for it in range(len(child_board[0])):
                    if child_board[0][it] == "W":
                        child_board[0][it] = "w"
                for it in range(len(child_board[7])):
                    if child_board[7][it] == "B":
                        child_board[7][it] = "b"
                child = Node(parent, child_board, color)
                child.last = [beats[i][2][0], beats[i][2][1]]
                children.append(child)
        for child in children:
            parents[pi].children.append(child)

        if not found_beat:
            for piece in pieces:
                moves = get_possible_reg_moves(copy.deepcopy(parent.board), piece)
                for i in range(0, len(moves)):
                    child_board = copy.deepcopy(parent.board)
                    if child_board[piece[1]][piece[0]] == color.lower():
                        child_board[moves[i][1][1]][moves[i][1][0]] = color.lower()
                    else:
                        child_board[moves[i][1][1]][moves[i][1][0]] = color
                    child_board[piece[1]][piece[0]] = "-"
                    for it in range(len(child_board[0])):
                        if child_board[0][it] == "W":
                            child_board[0][it] = "w"
                    for it in range(len(child_board[7])):
                        if child_board[7][it] == "B":
                            child_board[7][it] = "b"
                    child = Node(parent, child_board, color)
                    child.last = [moves[i][1][0], moves[i][1][1]]
                    children.append(child)
            for child in children:
                parents[pi].children.append(child)
    results = [found_beat]
    for p in parents:
        for c in p.children:
            results.append(c)
    return results


def get_all_beats(parent, color):
    """
    Returns all possible beats of player.

    :param parent: parent node
    :type parent: Node

    :param color: color of player to check beat
    :type color: string
    """
    pieces = get_pieces_positions(parent.board, color)
    all_beats = []
    for piece in pieces:
        beats = get_possible_beats(parent.board, piece)
        for beat in beats:
            all_beats.append(beat)
    return all_beats


def get_all_moves(parent, color):
    """
    Returns all possible regular moves of player.

    :param parent: parent node
    :type parent: Node

    :param color: color of player to check moves
    :type color: string
    """
    pieces = get_pieces_positions(parent.board, color)
    all_moves = []
    for piece in pieces:
        moves = get_possible_reg_moves(parent.board, piece)
        for beat in moves:
            all_moves.append(beat)
    return all_moves


def interprete_move(mv):
    """
    Interpretes player input move, and convertes it
    to proper indices in board arrays.

    :param mv: move input
    :type mv: string
    """
    try:
        move = []
        for i in mv:
            move.append(i)

        move[0] = ord(move[0]) - 96
        move[4] = ord(move[4]) - 96
        return [[move[0]-1, 8-int(move[1])], [move[4]-1, 8-int(move[5])]]
    except Exception:
        return -1


def player_move(parent):
    """
    Prompt player to make move and returns it.

    :param parent: root node
    :type parent: Node
    """
    while True:
        print("Your turn!")
        player_move = input("Make move: ")
        player_move = interprete_move(player_move)
        while player_move == -1:
            player_move = input("Make move: ")
            player_move = interprete_move(player_move)
        white_moves = get_all_beats(parent, "W")
        if white_moves != []:
            if len(white_moves[0]) == 3:
                coords = []
                for i in white_moves:
                    coords.append([i[0], i[1], i[2]])
        else:
            white_moves = get_all_moves(parent, "W")
            coords = []
            for i in white_moves:
                coords.append([i[0], i[1]])

        possible = False
        beat = None
        if len(coords[0]) == 3:
            for j in coords:
                if len(DeepDiff([j[0], j[2]], player_move)) == 0:
                    beat = j[1]
                    possible = True
        else:
            for j in coords:
                if len(DeepDiff(j, player_move)) == 0:
                    possible = True
        if not possible:
            print("Wrong move (eg. a3->b4)! (check if you put correct coordinates or have a possible beating of enemy piece)")
        else:
            if beat is not None:
                return player_move + [beat]
            return player_move


def check_if_maximize(color):
    """
    Checks if minimax should be maximizing
    or minimazing when checking next depth.

    :param color: color of player
    :type color: string
    """
    if color == "W":
        maximize = False
    elif color == "B":
        maximize = True
    return maximize


def minimax(parent, depth, alpha, beta, maximizing):
    """
    Minimax algorithm finds best move for computer player to move
    based on depth of searching the tree of possible moves.

    :param parent: root node
    :type parent: Node

    :param depth: depth of searching
    :type depth: int

    :param alpha: alpha parameter
    :type alpha: int / float

    :param beta: beta parameter
    :type beta: int / float

    :param maximizing: maximizing or minimizing parameter
    :type alpha: bool
    """
    if depth == 0 or parent.children == []:
        return parent.value
    if maximizing:
        all_eval_max = []
        eval_max = -inf
        for child in parent.children:
            maximize = check_if_maximize(child.color)
            eval1 = minimax(child, depth - 1, alpha, beta, maximize)
            if eval1 >= eval_max:
                eval_max = eval1
                all_eval_max = []
                all_eval_max.append(child)
            elif eval1 == eval_max:
                all_eval_max.append(child)
            alpha = max(eval1, alpha)
            if beta < alpha:
                break
        choose = ch(all_eval_max)
        choose.good = True
        return eval_max
    else:
        all_eval_min = []
        eval_min = inf
        for child in parent.children:
            maximize = check_if_maximize(child.color)
            eval2 = minimax(child, depth - 1, alpha, beta, maximize)
            if eval2 <= eval_min:
                eval_min = eval2
                all_eval_min = []
                all_eval_min.append(child)
            elif eval2 == eval_min:
                all_eval_min.append(child)
            beta = min(eval2, beta)
            if beta < alpha:
                break
        choose = ch(all_eval_min)
        choose.good = True
        return eval_min


def run(parent, depth):
    """
    Prompts player move then computer move,
    multibeating is obligatory.

    :param parent: parent node
    :type parent: Node

    :param depth: depth of minimax algorithm
    :type depth: int
    """
    # Human move
    clear()
    print_board(parent.board)
    pieces_black = get_pieces_positions(parent.board, "B")
    pieces_white = get_pieces_positions(parent.board, "W")
    if len(pieces_black) == 0:
        print("White won!")
        return
    if len(pieces_white) == 0:
        print("Black won!")
        return
    p_move = player_move(parent)
    tmp_board = copy.deepcopy(parent.board)
    if len(p_move) == 3:
        if tmp_board[p_move[0][1]][p_move[0][0]] == "w":
            tmp_board[p_move[1][1]][p_move[1][0]] = "w"
        else:
            tmp_board[p_move[1][1]][p_move[1][0]] = "W"
        tmp_board[p_move[0][1]][p_move[0][0]] = "-"
        tmp_board[p_move[2][1]][p_move[2][0]] = "-"
        for it in range(len(tmp_board[0])):
            if tmp_board[0][it] == "W":
                tmp_board[0][it] = "w"
        for it2 in range(len(tmp_board[7])):
            if tmp_board[7][it2] == "B":
                tmp_board[7][it2] = "b"
        next_beat = get_possible_beats(tmp_board, [p_move[1][0], p_move[1][1]])
        while len(next_beat) > 0:
            break_cond = False
            while not break_cond:
                clear()
                print_board(tmp_board)
                p_next_move = input("Make move:")
                p_next_move = interprete_move(p_next_move)
                for i in next_beat:
                    parse = ([i[0], i[2]])
                    if p_next_move == parse:
                        if tmp_board[i[0][1]][i[0][0]] == "w":
                            tmp_board[i[2][1]][i[2][0]] = "w"
                        else:
                            tmp_board[i[2][1]][i[2][0]] = "W"
                        tmp_board[i[0][1]][i[0][0]] = "-"
                        tmp_board[i[1][1]][i[1][0]] = "-"
                        for it in range(len(tmp_board[0])):
                            if tmp_board[0][it] == "W":
                                tmp_board[0][it] = "w"
                        for it2 in range(len(tmp_board[7])):
                            if tmp_board[7][it2] == "B":
                                tmp_board[7][it2] = "b"
                        break_cond = True
            next_beat = get_possible_beats(tmp_board, [p_next_move[1][0], p_next_move[1][1]])
    else:
        if tmp_board[p_move[0][1]][p_move[0][0]] == "w":
            tmp_board[p_move[1][1]][p_move[1][0]] = "w"
        else:
            tmp_board[p_move[1][1]][p_move[1][0]] = "W"
        tmp_board[p_move[0][1]][p_move[0][0]] = "-"
        for it in range(len(tmp_board[0])):
            if tmp_board[0][it] == "W":
                tmp_board[0][it] = "w"
        for it2 in range(len(tmp_board[7])):
            if tmp_board[7][it2] == "B":
                tmp_board[7][it2] = "b"
    parent = Node(parent, tmp_board, "W")
    clear()
    print_board(parent.board)

    # CPU move
    print("Computer thinking...")
    while True:
        root = copy.deepcopy(parent)
        pieces_black = get_pieces_positions(root.board, "B")
        pieces_white = get_pieces_positions(root.board, "W")
        if len(pieces_black) == 0:
            print("White won!")
            return
        if len(pieces_white) == 0:
            print("Black won!")
            return
        next_beats = get_all_beats(root, "B")
        beating = False
        if len(next_beats) > 0:
            beating = True
        parents = [False, root]
        d = 0
        while d < depth:
            parents = get_next_possible_moves(parents[1:], "B")
            if d == 0:
                first_parents = parents[:]
            type_beat = parents[0]
            d += 1
            while type_beat is True and d < depth:
                parents = get_next_possible_moves(parents[1:], "B")
                type_beat = parents[0]
                d += 1
            if d >= depth:
                break
            if depth % 2 == 1 and d > depth:
                break
            parents = get_next_possible_moves(parents[1:], "W")
            type_beat = parents[0]
            d += 1
            while type_beat is True and d < depth:
                parents = get_next_possible_moves(parents[1:], "W")
                type_beat = parents[0]
                d += 1
        minimax(root, depth, -inf, inf, True)
        parent = None
        for p in first_parents[1:]:
            if p.good:
                parent = copy.deepcopy(p)
                break

        next_beats = get_possible_beats(parent.board, parent.last)
        if len(next_beats) == 0 or beating is False:
            break

    if parent is not None:
        run(parent, depth)


if __name__ == "__main__":
    # CONFIGURATION
    depth = 4
    starting_parent = Node(None, board, "W")
    run(starting_parent, depth)
