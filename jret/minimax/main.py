import pygame
import sys
import constants as const
import numpy as np
from tic_tac_toe import game_state, antidiag, make_move, ai_move


def main():

    pygame.init()

    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")

    board = np.zeros((const.NROWS, const.NCOLS))

    screen.fill(const.DARK_CYAN)
    draw_grid(screen, const.CARRIBEAN_CURRENT)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONUP and event.button == const.LEFT_MOUSE_BUTTON:
                click_pos_x, click_pos_y = event.pos

                move_row = click_pos_y // const.TILE_SIZE
                move_col = click_pos_x // const.TILE_SIZE

                if not game_state(board)[0]:
                    try:
                        board = make_move(board, (move_row, move_col), const.PLAYER_X)
                    except ValueError:
                        continue

                    draw_cross(screen, move_row, move_col, const.SPACE_GREY)

                    pygame.display.update()

                if not game_state(board)[0]:

                    move = ai_move(board, const.PLAYER_O,
                                   algoritm=const.ALGORITHM,
                                   heur=const.HEURISTIC)

                    board = make_move(board, move, const.PLAYER_O)
                    draw_circle(screen, move[0], move[1], const.DIM_WHITE)

                    pygame.display.update()

        state, winner = game_state(board)
        if state:
            if winner != const.PLAYER_NEUTRAL:
                draw_win_line(screen, board, winner, const.DARK_RED)

        pygame.display.update()


def draw_grid(screen, line_color):
    # Vertical lines
    pygame.draw.line(screen, line_color,
                     (0, const.SCREEN_HEIGHT // 3),
                     (const.SCREEN_WIDTH, const.SCREEN_HEIGHT // 3),
                     const.GRID_LINE_WIDTH)

    pygame.draw.line(screen, line_color,
                     (0, 2 * const.SCREEN_HEIGHT // 3),
                     (const.SCREEN_WIDTH, 2 * const.SCREEN_HEIGHT // 3),
                     const.GRID_LINE_WIDTH)

    # Horizontal lines
    pygame.draw.line(screen, line_color,
                     (const.SCREEN_WIDTH // 3, 0),
                     (const.SCREEN_WIDTH // 3, const.SCREEN_HEIGHT),
                     const.GRID_LINE_WIDTH)

    pygame.draw.line(screen, line_color,
                     (2 * const.SCREEN_WIDTH // 3, 0),
                     (2 * const.SCREEN_WIDTH // 3, const.SCREEN_HEIGHT),
                     const.GRID_LINE_WIDTH)


def draw_circle(screen, row, col, color):
    x_coord = col * const.TILE_SIZE + const.TILE_SIZE // 2
    y_coord = row * const.TILE_SIZE + const.TILE_SIZE // 2

    pygame.draw.circle(screen, color, (x_coord, y_coord),
                       const.CIRCLE_RADIUS, const.CIRCLE_WIDTH)


def draw_cross(screen, row, col, color):
    x_coord = col * const.TILE_SIZE + const.TILE_SIZE // 2
    y_coord = row * const.TILE_SIZE + const.TILE_SIZE // 2

    pygame.draw.line(screen, color,
                     (x_coord - const.CROSS_SIZE, y_coord - const.CROSS_SIZE,),
                     (x_coord + const.CROSS_SIZE, y_coord + const.CROSS_SIZE),
                     const.CROSS_WIDTH)

    pygame.draw.line(screen, color,
                     (x_coord - const.CROSS_SIZE, y_coord + const.CROSS_SIZE,),
                     (x_coord + const.CROSS_SIZE, y_coord - const.CROSS_SIZE),
                     const.CROSS_WIDTH)


def find_win_location(board, winner):

    for i in range(board.shape[0]):
        if np.all(board[i, :] == winner):
            return i, None

        elif np.all(board[:, i] == winner):
            return None, i

    if np.all(np.diag(board) == winner):
        return 0, 0

    if np.all(antidiag(board) == winner):
        return 2, 0


def draw_win_line(screen, board, winner, win_line_color):

    row, col = find_win_location(board, winner)

    if col is None:
        y_coord = row * const.TILE_SIZE + const.TILE_SIZE // 2
        x_coord = 0
        pygame.draw.line(screen, win_line_color, (x_coord, y_coord),
                         (x_coord + const.SCREEN_WIDTH, y_coord), const.WIN_LINE_WIDTH)

    elif row is None:
        x_coord = col * const.TILE_SIZE + const.TILE_SIZE // 2
        y_coord = 0
        pygame.draw.line(screen, win_line_color, (x_coord, y_coord),
                         (x_coord, y_coord + const.SCREEN_HEIGHT), const.WIN_LINE_WIDTH)

    elif row == col:

        pygame.draw.line(screen, win_line_color, (0, 0),
                         (const.SCREEN_HEIGHT, const.SCREEN_WIDTH), const.WIN_LINE_WIDTH)

    else:

        pygame.draw.line(screen, win_line_color, (const.SCREEN_HEIGHT, 0),
                         (0, const.SCREEN_WIDTH), const.WIN_LINE_WIDTH)


if __name__ == "__main__":
    main()
