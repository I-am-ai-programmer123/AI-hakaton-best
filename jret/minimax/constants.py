SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
NROWS = 3
NCOLS = 3
TILE_SIZE = SCREEN_HEIGHT // NROWS

GRID_LINE_WIDTH = 20

WIN_LINE_WIDTH = 20

CIRCLE_RADIUS = 90
CIRCLE_WIDTH = 20

CROSS_SIZE = 80
CROSS_WIDTH = 25

DARK_RED = (139, 0, 0)
PURE_WHITE = (255, 255, 255)
DIM_WHITE = (190, 190, 190)
DARK_TURQUOISE = (28, 170, 156)
DARK_CYAN = (23, 145, 135)
TEAL = (0, 128, 128)
SPACE_GREY = (52, 61, 70)
LIGHT_SEA_GREEN = (32, 178, 170)
CARRIBEAN_CURRENT = (0, 109, 111)

LEFT_MOUSE_BUTTON = 1

PLAYER_X = 1  # must be positive
PLAYER_O = -1  # must be negative
PLAYER_NEUTRAL = 0  # must be zero

MINIMAX_MAX_DEPTH = 4  # can't be 0 or less otherwise, algorithm won't work
ALGORITHM = "minimax"  # can be "minimax", "alpha-beta" or "alpha-beta-memo" 
HEURISTIC = "tile_weights"  # can be tile_weights or win_moves