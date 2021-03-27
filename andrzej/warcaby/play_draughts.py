#!/usr/bin/env python3

from math import inf
from minimax_algorithm import MiniMax, positionOver


def drawBoard(board):
    print("    a    b    c    d    e    f    g    h")
    for idx, row in enumerate(board):
        print(f"{idx+1} {row}")
    print()


def play(board):
    playerMove = True
    while not positionOver(board):
        if playerMove:
            drawBoard(board)

            pawn = input("Pawn to move: ")
            if pawn == 'quit':
                print("Black won!")
                break

            destination = input("Where to move a pawn: ")

            px = ord(pawn[0]) - 97
            py = int(pawn[1]) - 1

            dx = ord(destination[0]) - 97
            dy = int(destination[1]) - 1

            vec = [dy - py, dx - px]

            # man move
            if board[py][px] == 'w':
                board[py][px] = '.'
                board[dy][dx] = 'w'

                while vec[0] > 1:
                    if vec[1] > 0:
                        board[py+1][px+1] = '.'
                    elif vec[1] < 0:
                        board[py+1][px-1] = '.'

                    drawBoard(board)
                    ans = input("Can you do a mulit-jump?[y/n] ")
                    vec = [0, 0]
                    if ans[0] == 'y':
                        destination = input("Where to move a pawn: ")

                        py, px = dy, dx

                        dx = ord(destination[0]) - 97
                        dy = int(destination[1]) - 1

                        vec = [dy - py, dx - px]

                        board[py][px] = '.'
                        board[dy][dx] = 'w'

                if dy == len(board)-1:
                    board[dy][dx] = 'W'

            # queen move
            elif board[py][px] == 'W':
                board[py][px] = '.'
                board[dy][dx] = 'W'

                # move left up
                if vec[0] < 0 and vec[1] < 0:
                    for i in range(1, vec[0]):
                        if board[py-i][px-i] == 'b' or board[py-i][px-i] == 'B':
                            board[py-i][px-i] = '.'
                # move right up
                if vec[0] < 0 and vec[1] < 0:
                    for i in range(1, vec[0]):
                        if board[py-i][px+i] == 'b' or board[py-i][px+i] == 'B':
                            board[py-i][px+i] = '.'
                # move left down
                if vec[0] > 0 and vec[1] < 0:
                    for i in range(1, vec[0]):
                        if board[py+i][px-i] == 'b' or board[py+i][px-i] == 'B':
                            board[py+i][px-i] = '.'
                # move right down
                if vec[0] > 0 and vec[1] > 0:
                    for i in range(1, vec[0]):
                        if board[py+i][px+i] == 'b' or board[py+i][px+i] == 'B':
                            board[py+i][px+i] = '.'

            drawBoard(board)

        else:
            eval, board = MiniMax(board, 8, -inf, inf, True)
            if board is None:
                print("White won!")
                break

        playerMove = not playerMove

    if playerMove:
        print("Black won!")
    else:
        print("White won!")


if __name__ == "__main__":
    board = [
            [' ', 'w', ' ', 'w', ' ', 'w', ' ', 'w'],
            ['w', ' ', 'w', ' ', 'w', ' ', 'w', ' '],
            [' ', 'w', ' ', 'w', ' ', 'w', ' ', 'w'],
            ['.', ' ', '.', ' ', '.', ' ', '.', ' '],
            [' ', '.', ' ', '.', ' ', '.', ' ', '.'],
            ['b', ' ', 'b', ' ', 'b', ' ', 'b', ' '],
            [' ', 'b', ' ', 'b', ' ', 'b', ' ', 'b'],
            ['b', ' ', 'b', ' ', 'b', ' ', 'b', ' ']
            ]

    play(board)
