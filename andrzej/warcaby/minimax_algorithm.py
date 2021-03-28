from math import inf
from copy import deepcopy


def positionOver(position):
    nWhites = 0
    nBlacks = 0
    for row in position:
        for pawn in row:
            if pawn == 'w':
                nWhites += 1
            if pawn == 'b':
                nBlacks += 1

    if nBlacks == 0:
        return True
    if nWhites == 0:
        return True

    return False


def evaluate(position):
    evaluation = 0
    for row in position:
        for pawn in row:
            if pawn == 'w':
                evaluation -= 1
            if pawn == 'W':
                evaluation -= 2
            if pawn == 'b':
                evaluation += 1
            if pawn == 'B':
                evaluation += 2

    return evaluation


def whiteCapture(position, wPos, bPos):
    nextMoves = []
    nextPos = [2*bPos[0] - wPos[0], 2*bPos[1] - wPos[1]]
    if nextPos[0] >= 0 and nextPos[0] < len(position) and nextPos[1] >= 0 and nextPos[1] < len(position[0]):
        if position[nextPos[0]][nextPos[1]] == '.':
            position[bPos[0]][bPos[1]] = '.'
            position[wPos[0]][wPos[1]] = '.'
            position[nextPos[0]][nextPos[1]] = 'w'
            if nextPos[0] == len(position)-1:
                position[nextPos[0]][nextPos[1]] = 'W'
        else:
            return nextMoves
    else:
        return nextMoves

    y = nextPos[0]
    x = nextPos[1]
    if (y+1 < len(position) and x-1 >= 0) and (position[y+1][x-1] == 'b' or position[y+1][x-1] == 'B'):
        nextMoves += whiteCapture(deepcopy(position), [y, x], [y+1, x-1])
    if (y+1 < len(position) and x+1 < len(position[0])) and (position[y+1][x+1] == 'b' or position[y+1][x+1] == 'B'):
        nextMoves += whiteCapture(deepcopy(position), [y, x], [y+1, x+1])
    else:
        nextMoves.append(position)

    return nextMoves


def blackCapture(position, bPos, wPos):
    nextMoves = []
    nextPos = [2*wPos[0] - bPos[0], 2*wPos[1] - bPos[1]]
    if nextPos[0] >= 0 and nextPos[0] < len(position) and nextPos[1] >= 0 and nextPos[1] < len(position[0]):
        if position[nextPos[0]][nextPos[1]] == '.':
            position[wPos[0]][wPos[1]] = '.'
            position[bPos[0]][bPos[1]] = '.'
            position[nextPos[0]][nextPos[1]] = 'b'
            if nextPos[0] == 0:
                position[nextPos[0]][nextPos[1]] = 'B'
        else:
            return nextMoves
    else:
        return nextMoves

    y = nextPos[0]
    x = nextPos[1]
    if (y-1 < len(position) and x-1 >= 0) and (position[y-1][x-1] == 'w' or position[y-1][x-1] == 'W'):
        nextMoves += blackCapture(deepcopy(position), [y, x], [y-1, x-1])
    if (y-1 < len(position) and x+1 < len(position[0])) and (position[y-1][x+1] == 'w' or position[y-1][x+1] == 'W'):
        nextMoves += blackCapture(deepcopy(position), [y, x], [y-1, x+1])
    else:
        nextMoves.append(position)

    return nextMoves


def getNextWhiteMoves(position):
    nextMoves = []
    for y in range(len(position)):
        for x in range(len(position[0])):
            # man move
            if position[y][x] == 'w':
                # forward left move
                if y+1 < len(position) and x-1 >= 0:
                    if position[y+1][x-1] == 'w' or position[y+1][x-1] == 'W':
                        pass
                    elif position[y+1][x-1] == '.':
                        move = deepcopy(position)
                        move[y+1][x-1] = 'w'
                        move[y][x] = '.'
                        if y+1 == len(position)-1:
                            move[y+1][x-1] = 'W'
                        nextMoves.append(move)
                    elif position[y+1][x-1] == 'b' or position[y+1][x-1] == 'B':
                        nextMoves += whiteCapture(deepcopy(position), [y, x], [y+1, x-1])

                # forward right move
                if y+1 < len(position) and x+1 < len(position[0]):
                    if position[y+1][x+1] == 'w' or position[y+1][x+1] == 'W':
                        pass
                    elif position[y+1][x+1] == '.':
                        move = deepcopy(position)
                        move[y+1][x+1] = 'w'
                        move[y][x] = '.'
                        if y+1 == len(position)-1:
                            move[y+1][x+1] = 'W'
                        nextMoves.append(move)
                    elif position[y+1][x+1] == 'b' or position[y+1][x+1] == 'B':
                        nextMoves += whiteCapture(deepcopy(position), [y, x], [y+1, x+1])

            # moves for a King
            elif position[y][x] == 'W':
                # move left up
                i = 1
                while y-i >= 0 and x-i >= 0:
                    if position[y-i][x-i] == 'w' or position[y-i][x-i] == 'W':
                        break
                    if position[y-i][x-i] == '.':
                        move = deepcopy(position)
                        move[y-i][x-i] = 'W'
                        move[y][x] = '.'
                        nextMoves.append(move)
                    elif position[y-i][x-i] == 'b' or position[y-i][x-i] == 'B':
                        if (y-i-1 >= 0 and x-i-1 >= 0) and position[y-i-1][x-i-1] == '.':
                            move = deepcopy(position)
                            move[y-i][x-i] == '.'
                            move[y][x] = '.'
                            i += 1
                            move[y-i][x-i] == 'W'
                            nextMoves.append(move)
                    i += 1
                # move right up
                i = 1
                while y-i >= 0 and x+i < len(position[0]):
                    if position[y-i][x+i] == 'w' or position[y-i][x+i] == 'W':
                        break
                    if position[y-i][x+i] == '.':
                        move = deepcopy(position)
                        move[y-i][x+i] = 'W'
                        move[y][x] = '.'
                        nextMoves.append(move)
                    elif position[y-i][x+i] == 'b' or position[y-i][x+i] == 'B':
                        if (y-i-1 >= 0 and x+i+1 < len(position[0])) and position[y-i-1][x+i+1] == '.':
                            move = deepcopy(position)
                            move[y-i][x+i] == '.'
                            move[y][x] = '.'
                            i += 1
                            move[y-i][x+i] == 'W'
                            nextMoves.append(move)
                    i += 1
                # move left down
                i = 1
                while y+i < len(position) and x-i >= 0:
                    if position[y+i][x-i] == 'w' or position[y+i][x-i] == 'W':
                        break
                    if position[y+i][x-i] == '.':
                        move = deepcopy(position)
                        move[y+i][x-i] = 'W'
                        move[y][x] = '.'
                        nextMoves.append(move)
                    elif position[y+i][x-i] == 'b' or position[y+i][x-i] == 'B':
                        if (y+i+1 < len(position) and x-i-1 >= 0) and position[y+i+1][x-i-1] == '.':
                            move = deepcopy(position)
                            move[y+i][x-i] == '.'
                            move[y][x] = '.'
                            i += 1
                            move[y+i][x-i] == 'W'
                            nextMoves.append(move)
                    i += 1
                # move right down
                i = 1
                while y+i < len(position) and x+i < len(position[0]):
                    if position[y+i][x+i] == 'w' or position[y+i][x+i] == 'W':
                        break
                    if position[y+i][x+i] == '.':
                        move = deepcopy(position)
                        move[y+i][x+i] = 'W'
                        move[y][x] = '.'
                        nextMoves.append(move)
                    elif position[y+i][x+i] == 'b' or position[y+i][x+i] == 'B':
                        if (y+i+1 < len(position) and x+i+1 < len(position[0])) and position[y+i+1][x+i+1] == '.':
                            move = deepcopy(position)
                            move[y+i][x+i] == '.'
                            move[y][x] = '.'
                            i += 1
                            move[y+i][x+i] == 'W'
                            nextMoves.append(move)
                    i += 1

    return nextMoves


def getNextBlackMoves(position):
    nextMoves = []
    for y in range(len(position)):
        for x in range(len(position[0])):
            # man move
            if position[y][x] == 'b':
                # forward left move
                if y-1 >= 0 and x-1 >= 0:
                    if position[y-1][x-1] == 'b' or position[y-1][x-1] == 'B':
                        pass
                    elif position[y-1][x-1] == '.':
                        move = deepcopy(position)
                        move[y-1][x-1] = 'b'
                        move[y][x] = '.'
                        if y-1 == 0:
                            move[y-1][x-1] = 'B'
                        nextMoves.append(move)
                    elif position[y-1][x-1] == 'w' or position[y-1][x-1] == 'W':
                        nextMoves += blackCapture(deepcopy(position), [y, x], [y-1, x-1])

                # forward right move
                if y-1 >= 0 and x+1 < len(position[0]):
                    if position[y-1][x+1] == 'b' or position[y-1][x+1] == 'B':
                        pass
                    elif position[y-1][x+1] == '.':
                        move = deepcopy(position)
                        move[y-1][x+1] = 'b'
                        move[y][x] = '.'
                        if y-1 == 0:
                            move[y-1][x+1] = 'B'
                        nextMoves.append(move)
                    elif position[y-1][x+1] == 'w' or position[y-1][x+1] == 'W':
                        nextMoves += blackCapture(deepcopy(position), [y, x], [y-1, x+1])

            # moves for a King
            elif position[y][x] == 'B':
                # move left up
                i = 1
                while y-i >= 0 and x-i < len(position[0]):
                    if position[y-i][x-i] == 'b' or position[y-i][x-i] == 'B':
                        break
                    if position[y-i][x-i] == '.':
                        move = deepcopy(position)
                        move[y-i][x-i] = 'B'
                        move[y][x] = '.'
                        nextMoves.append(move)
                    elif position[y-i][x-i] == 'w' or position[y-i][x-i] == 'W':
                        if (y-i-1 >= 0 and x-i-1 < len(position[0])) and position[y-i-1][x-i-1] == '.':
                            move = deepcopy(position)
                            move[y-i][x-i] == '.'
                            move[y][x] = '.'
                            i += 1
                            move[y-i][x-i] == 'B'
                            nextMoves.append(move)
                    i += 1
                # move right up
                i = 1
                while y-i >= 0 and x+i < len(position[0]):
                    if position[y-i][x+i] == 'b' or position[y-i][x+i] == 'B':
                        break
                    if position[y-i][x+i] == '.':
                        move = deepcopy(position)
                        move[y-i][x+i] = 'B'
                        move[y][x] = '.'
                        nextMoves.append(move)
                    elif position[y-i][x+i] == 'w' or position[y-i][x+i] == 'W':
                        if (y-i-1 >= 0 and x+i+1 < len(position[0])) and position[y-i-1][x+i+1] == '.':
                            move = deepcopy(position)
                            move[y-i][x+i] == '.'
                            move[y][x] = '.'
                            i += 1
                            move[y-i][x+i] == 'B'
                            nextMoves.append(move)
                    i += 1
                # move left down
                i = 1
                while y+i < len(position) and x-i >= 0:
                    if position[y+i][x-i] == 'b' or position[y+i][x-i] == 'B':
                        break
                    if position[y+i][x-i] == '.':
                        move = deepcopy(position)
                        move[y+i][x-i] = 'B'
                        move[y][x] = '.'
                        nextMoves.append(move)
                    elif position[y+i][x-i] == 'w' or position[y+i][x-i] == 'W':
                        if (y+i+1 < len(position) and x-i-1 >= 0) and position[y+i+1][x-i-1] == '.':
                            move = deepcopy(position)
                            move[y+i][x-i] == '.'
                            move[y][x] = '.'
                            i += 1
                            move[y+i][x-i] == 'B'
                            nextMoves.append(move)
                    i += 1
                # move right down
                i = 1
                while y+i < len(position) and x+i < len(position[0]):
                    if position[y+i][x+i] == 'b' or position[y+i][x+i] == 'B':
                        break
                    if position[y+i][x+i] == '.':
                        move = deepcopy(position)
                        move[y+i][x+i] = 'B'
                        move[y][x] = '.'
                        nextMoves.append(move)
                    elif position[y+i][x+i] == 'w' or position[y+i][x+i] == 'W':
                        if (y+i+1 < len(position) and x+i+1 < len(position[0])) and position[y+i+1][x+i+1] == '.':
                            move = deepcopy(position)
                            move[y+i][x+i] == '.'
                            move[y][x] = '.'
                            i += 1
                            move[y+i][x+i] == 'B'
                            nextMoves.append(move)
                    i += 1

    return nextMoves


def MiniMax(position, depth, alpha, beta, maximizingPlayer):
    bestPos = None
    if depth == 0 or positionOver(position):
        return evaluate(position), position

    if maximizingPlayer:
        maxEval = -inf
        nextPositions = getNextBlackMoves(position)
        for child in nextPositions:
            eval, x = MiniMax(child, depth - 1, alpha, beta, False)
            if eval > maxEval:
                maxEval = eval
                bestPos = child
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, bestPos

    else:
        minEval = inf
        nextPositions = getNextWhiteMoves(position)
        for child in nextPositions:
            eval, x = MiniMax(child, depth - 1, alpha, beta, True)
            if eval < minEval:
                minEval = eval
                bestPos = child
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, bestPos
