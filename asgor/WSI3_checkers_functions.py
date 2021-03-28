import copy

# field = [
# ['_', '_', '_', '_', 'WQ', '_', '_', '_'],   # 0
# ['_', 'B', '_', 'B', '_', 'B', '_', '_'],   # 1
# ['_', '_', '_', '_', '_', '_', '_', '_'],   # 2
# ['_', '_', '_', 'B', '_', 'B', '_', '_'],   # 3
# ['B', '_', '_', '_', '_', '_', '_', '_'],   # 4
# ['_', 'B', '_', 'B', '_', '_', '_', '_'],   # 5
# ['_', '_', 'W', '_', '_', '_', '_', '_'],   # 6
# ['_', '_', '_', '_', '_', '_', '_', '_']    # 7
# ]
# 0    1    2    3    4    5    6    7

def white_reg_beat_left(field, X, Y):
    if Y-2 < 0 or X-2 < 0:
        return False
    return field[Y-1][X-1] in ['B', 'BQ'] and field[Y-2][X-2] == "_"

def white_reg_beat_right(field, X, Y):
    if Y-2 < 0 or X+2 >= len(field):
        return False
    return field[Y-1][X+1] in ['B', 'BQ'] and field[Y-2][X+2] == "_"

#white queen
def white_queen_beat_left(field, X, Y):
    if Y+2 >= len(field) or X-2 < 0:
        return False
    return field[Y+1][X-1] in ['B', 'BQ'] and field[Y+2][X-2] == "_"

def white_queen_beat_right(field, X, Y):
    if Y+2 >= len(field) or X+2 >= len(field):
        return False
    return field[Y+1][X+1] in ['B', 'BQ'] and field[Y+2][X+2] == "_"

#black regular
def black_reg_beat_left(field, X, Y):
    if Y+2 >= len(field) or X-2 < 0:
        return False
    return field[Y+1][X-1] in ['W', 'WQ'] and field[Y+2][X-2] == '_'

def black_reg_beat_right(field, X, Y):
    if Y+2 >= len(field) or X+2 >= len(field):
        return False
    return field[Y+1][X+1] in ['W', 'WQ'] and field[Y-2][X+2] == '_'

#black queen
def black_queen_beat_left(field, X, Y):
    if Y-2 < 0 or X-2 < 0:
        return False
    return field[Y-1][X-1] in ['W', 'WQ'] and field[Y-2][X-2] == '_'

def black_queen_beat_right(field, X, Y):
    if Y-2 < 0 or X+2 >= len(field):
        return False
    return field[Y-1][X+1] in ['W', 'WQ'] and field[Y-2][X+2] == '_'


def beating_moves_white_reg(field, c_m):
    X = int(c_m[-2])
    Y = int(c_m[-1])
    # print(X, Y)
    if white_reg_beat_left(field, X, Y) == False and white_reg_beat_right(field, X, Y) == False:
        return [c_m]
    elif white_reg_beat_left(field, X, Y) and white_reg_beat_right(field, X, Y):
        return beating_moves_white_reg(field, c_m + str(X-2) + str(Y-2)) + beating_moves_white_reg(field, c_m + str(X+2) + str(Y-2))
    elif white_reg_beat_left(field, X, Y):
        return beating_moves_white_reg(field, c_m + str(X-2) + str(Y-2))
    elif white_reg_beat_right(field, X, Y):
        return beating_moves_white_reg(field, c_m + str(X+2) + str(Y-2))

def beating_moves_white_queen(field, c_m):
    X = int(c_m[-2])
    Y = int(c_m[-1])

    # print(X, Y)
    if white_queen_beat_left(field, X, Y) == False and white_queen_beat_right(field, X, Y) == False:
        return [c_m]
    elif white_queen_beat_left(field, X, Y) and white_queen_beat_right(field, X, Y):
        return beating_moves_white_queen(field, c_m + str(X-2) + str(Y+2)) + beating_moves_white_queen(field, c_m + str(X+2) + str(Y+2))
    elif white_queen_beat_left(field, X, Y):
        return beating_moves_white_queen(field, c_m + str(X-2) + str(Y+2))
    elif white_queen_beat_right(field, X, Y):
        return beating_moves_white_queen(field, c_m + str(X+2) + str(Y+2))

# print(white_queen_beat_right(field, 2, 2))
# print(beating_moves_white_queen(field, '40'))

def beating_moves_black_reg(field, c_m):
    X = int(c_m[-2])
    Y = int(c_m[-1])
    # print(X, Y)
    if black_reg_beat_left(field, X, Y) == False and black_reg_beat_right(field, X, Y) == False:
        return [c_m]
    elif black_reg_beat_left(field, X, Y) and black_reg_beat_right(field, X, Y):
        return beating_moves_black_reg(field, c_m + str(X-2) + str(Y+2)) + beating_moves_black_reg(field, c_m + str(X+2) + str(Y+2))
    elif black_reg_beat_left(field, X, Y):
        return beating_moves_black_reg(field, c_m + str(X-2) + str(Y+2))
    elif black_reg_beat_right(field, X, Y):
        return beating_moves_black_reg(field, c_m + str(X+2) + str(Y+2))

def beating_moves_black_queen(field, c_m):
    X = int(c_m[-2])
    Y = int(c_m[-1])
    # print(X, Y)
    if black_queen_beat_left(field, X, Y) == False and black_queen_beat_right(field, X, Y) == False:
        return [c_m]
    elif black_queen_beat_left(field, X, Y) and black_queen_beat_right(field, X, Y):
        return beating_moves_black_queen(field, c_m + str(X-2) + str(Y-2)) + beating_moves_black_queen(field, c_m + str(X+2) + str(Y-2))
    elif black_queen_beat_left(field, X, Y):
        return beating_moves_black_queen(field, c_m + str(X-2) + str(Y-2))
    elif black_queen_beat_right(field, X, Y):
        return beating_moves_black_queen(field, c_m + str(X+2) + str(Y-2))


def generate_beating_moves_white(field):
    beating_moves = []
    for y in range(len(field)):
        for x in range(len(field)):
            if field[y][x] == 'W':
                if white_reg_beat_left(field, x, y) or white_reg_beat_right(field, x, y):
                    beating_moves.extend(beating_moves_white_reg(field, str(x)+str(y)))
            elif field[y][x] == 'WQ':
                if white_queen_beat_left(field, x, y) or white_queen_beat_right(field, x, y):
                    beating_moves.extend(beating_moves_white_queen(field, str(x)+str(y)))
    return beating_moves


def generate_beating_moves_black(field):
    beating_moves = []
    for y in range(len(field)):
        for x in range(len(field)):
            if field[y][x] == 'B':
                if black_reg_beat_left(field, x, y) or black_reg_beat_right(field, x, y):
                    beating_moves.extend(beating_moves_black_reg(field, str(x)+str(y)))
            elif field[y][x] == 'BQ':
                if black_queen_beat_left(field, x, y) or black_queen_beat_right(field, x, y):
                    beating_moves.extend(beating_moves_black_queen(field, str(x)+str(y)))
    return beating_moves

def generate_nonbeating_moves_white(field):
    moves = []
    for y in range(len(field)):
        for x in range(len(field)):
            if field[y][x] == 'W':
                if y-1 >= 0 and x-1 >= 0:
                    if field[y-1][x-1] == '_':
                        moves.append(str(x)+str(y)+str(x-1)+str(y-1))
                if y-1 >= 0 and x+1 < len(field):
                    if field[y-1][x+1] == '_':
                        moves.append(str(x)+str(y)+str(x+1)+str(y-1))
            elif field[y][x] == 'WQ':
                if x-1 >= 0 and y+1 < len(field):
                    if field[y+1][x-1] == '_':
                        moves.append(str(x)+str(y)+str(x-1)+str(y+1))
                if x+1 < len(field) and y+1 < len(field):
                    if field[y+1][x+1] == '_':
                        moves.append(str(x)+str(y)+str(x+1)+str(y+1))
    return moves

def generate_nonbeating_moves_black(field):
    moves = []
    for y in range(len(field)):
        for x in range(len(field)):
            if field[y][x] == 'B':
                if y+1 < len(field) and x-1 >= 0:
                    if field[y+1][x-1] == '_':
                       moves.append(str(x)+str(y)+str(x-1)+str(y+1))
                if x+1 < len(field) and y+1 < len(field):
                    if field[y+1][x+1] == '_':
                        moves.append(str(x)+str(y)+str(x+1)+str(y+1))
            elif field[y][x] == 'BQ':
                if x-1 >= 0 and y-1 >= 0:
                    if field[y-1][x-1] == '_':
                        moves.append(str(x)+str(y)+str(x-1)+str(y-1))
                if x+1 < len(field) and y-1 >= 0:
                    if field[y-1][x+1] == '_':
                        moves.append(str(x)+str(y)+str(x+1)+str(y-1))
    return moves

def generate_white_moves(field):
    moves = []
    moves.extend(generate_beating_moves_white(field))
    if not moves:
        moves.extend(generate_nonbeating_moves_white(field))
    return moves

def generate_black_moves(field):
    moves = []
    moves.extend(generate_beating_moves_black(field))
    if not moves:
        moves.extend(generate_nonbeating_moves_black(field))
    return moves

def generate_new_field(field, m):
    tfield = copy.deepcopy(field)
    if abs(int(m[0]) - int(m[2])) == 1:
        x1 = int(m[0])
        y1 = int(m[1])
        x2 = int(m[2])
        y2 = int(m[3])
        tfield[y2][x2] = field[y1][x1]
        tfield[y1][x1] = '_'
        return tfield
    for i in range(3, len(m), 2):
        x0 = int(m[i-3])
        y0 = int(m[i-2])
        x2 = int(m[i-1])
        y2 = int(m[i])
        x1 = x0 + ((x2 - x0) // 2)
        y1 = y0 + ((y2 - y0) // 2)
        tfield[y2][x2] = tfield[y0][x0]
        tfield[y1][x1] = '_'
        tfield[y0][x0] = '_'
    
    for i in range(len(field)):
        if tfield[0][i] == 'W':
            tfield[0][i] = 'WQ'
        if tfield[len(field)-1][i] == 'B':
            tfield[len(field)-1][i] = 'BQ'
    return tfield

        
def print_field(field):
    for y in range(len(field)):
        print(field[y], y)
    x = [str(i) for i in range(len(field))]
    print(x)

def rate_field(field):
    value = 0
    for y in range(len(field)):
        for x in range(len(field)):
            if field[y][x] == 'WQ':
                value -= 2
            elif field[y][x] == 'BQ':
                value += 2
            elif field[y][x] == 'W' and y <= len(field) // 2:
                value -= 1
            elif field[y][x] == 'B' and y >= len(field) // 2:
                value += 1
    return value

# wmoves = generate_white_moves(field)
# print(wmoves)

# print_field(field)
# print("---------------")

# print_field(generate_new_field(field, '402244'))