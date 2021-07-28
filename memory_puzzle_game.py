import random
from itertools import product
import pygame as pg
from pygame.locals import *
from pygame.color import Color

# Declaring the dimensions of the board and screen of the game
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 1000
SQUARE_SIZE = 70
SQUARE_GAP = 10
BOARD_WIDTH = 8
BOARD_HEIGHT = 4
X_MARG = (SCREEN_WIDTH - (BOARD_WIDTH * (SQUARE_SIZE + SQUARE_GAP))) // 2
Y_MARG = (SCREEN_HEIGHT - (BOARD_HEIGHT * (SQUARE_SIZE + SQUARE_GAP))) // 2

# the board size must be even due to pairs
assert (BOARD_HEIGHT * BOARD_WIDTH) % 2 == 0, 'The board size must always be even'

# the shapes required in the game
SQUARE = 'square'
CIRCLE = 'circle'
TRIANGLE = 'triangle'
DIAMOND = 'diamond'

BGCOLOR = Color('BLACK')

# Declaring function when the game is won and resetting the shapes
def game_won(revealed):
    return all(all(x) for x in revealed)

# function declared at the sart of the game
def start_game_animation(board):
    """Starts game by randomly showing 5 squares"""

    coordinates = list(product(range(BOARD_HEIGHT), range(BOARD_WIDTH)))
    random.shuffle(coordinates)

    revealed = [[False] * BOARD_WIDTH for i in range(BOARD_HEIGHT)]

    screen.fill(BGCOLOR)
    draw_board(board, revealed)
    #pygame imported as pg
    pg.display.update() 
    pg.time.wait(500)

    for sz in range(0, BOARD_HEIGHT * BOARD_WIDTH, 5):
        l = coordinates[sz: sz + 5]
        for x in l:
            revealed[x[0]][x[1]] = True
            draw_square(board, revealed, *x)
        pg.time.wait(500)
        for x in l:
            revealed[x[0]][x[1]] = False
            draw_square(board, revealed, *x)

# function declared been followed after game is won
def game_won_animation(board, revealed):
    """ Flashing background colors when the game is won"""

    color1 = Color('ANTIQUEWHITE')
    color2 = Color('BLACK')
    for i in range(10):
        color1,color2 = color2,color1
        screen.fill(color1)
        draw_board(board, revealed)
        pg.display.update()
        pg.time.wait(300)

# function to set-up board
def get_random_board(shape, colors):
    """ Generates the board by random shuffling"""

    icons = list(product(shape, colors))
    num_icons = BOARD_HEIGHT * BOARD_WIDTH // 2
    icons = icons[:num_icons] * 2

    random.shuffle(icons)
    board = [icons[i:i + BOARD_WIDTH]
             for i in range(0, BOARD_HEIGHT * BOARD_WIDTH, BOARD_WIDTH)]
    return board


def get_coord(x, y):
    """ Gets the coordinates of particular square.
        The squares are numbered height wise and then width wise.
        So the x and y are interchanged accordingly."""

    top = X_MARG + y * (SQUARE_SIZE + SQUARE_GAP)
    left = Y_MARG + x * (SQUARE_SIZE + SQUARE_GAP)
    return top, left


def draw_icon(icon, x, y):
    """Draws the icon of (x, y) square"""

    px, py = get_coord(x, y)
    if icon[0] == DIAMOND:
        pg.draw.polygon(screen, icon[1],
                            ((px + SQUARE_SIZE // 2, py + 5), (px + SQUARE_SIZE - 5, py + SQUARE_SIZE // 2),
                             (px + SQUARE_SIZE // 2, py + SQUARE_SIZE - 5), (px + 5, py + SQUARE_SIZE // 2)))
    elif icon[0] == SQUARE:
        pg.draw.rect(screen, icon[1],
                         (px + 5, py + 5, SQUARE_SIZE - 10, SQUARE_SIZE - 10))
    elif icon[0] == TRIANGLE:
        pg.draw.polygon(screen, icon[1],
                            ((px + SQUARE_SIZE // 2, py + 5), (px + 5, py + SQUARE_SIZE - 5),
                             (px + SQUARE_SIZE - 5, py + SQUARE_SIZE - 5)))
    elif icon[0] == CIRCLE:
        pg.draw.circle(screen, icon[1],
                           (px + SQUARE_SIZE // 2, py + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)


def get_pos(cx, cy):
    if cx < X_MARG or cy < Y_MARG:
        return None, None

    x = (cy - Y_MARG) // (SQUARE_SIZE + SQUARE_GAP)
    y = (cx - X_MARG) // (SQUARE_SIZE + SQUARE_GAP)

    if x >= BOARD_HEIGHT or y >= BOARD_WIDTH or(cx - X_MARG) % (SQUARE_SIZE + SQUARE_GAP) > SQUARE_SIZE or (cy - Y_MARG) % (SQUARE_SIZE + SQUARE_GAP) > SQUARE_SIZE:
        return None, None
    else:
        return x, y

def draw_square(board, revealed, x, y):
    """Draws a particular square"""

    coords = get_coord(x, y)
    square_rect = (*coords, SQUARE_SIZE, SQUARE_SIZE)
    pg.draw.rect(screen, BGCOLOR, square_rect)
    if revealed[x][y]:
        draw_icon(board[x][y], x, y)
    else:
        pg.draw.rect(screen, Color('darkgray'), square_rect)
    pg.display.update(square_rect)

def draw_board(board, revealed):
    """Draws the entire board"""

    for x in range(BOARD_HEIGHT):
        for y in range(BOARD_WIDTH):
            draw_square(board, revealed, x, y)

def draw_select_box(x, y):
    """Draws the highlight box around the square"""

    px, py = get_coord(x, y)
    pg.draw.rect(screen, Color('red'), (px - 5, py - 5, SQUARE_SIZE + 10, SQUARE_SIZE + 10), 5)


# the main function
def main():
    global screen, clock

    pg.init()

    screen = pg.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
    pg.display.set_caption('Memory Game')

    clock = pg.time.Clock()

    shape = (DIAMOND, SQUARE, TRIANGLE, CIRCLE)
    colors = (Color('red'), Color('yellow'), Color('orange'), Color('turquoise'))

    # There should be enough symbols
    assert len(shape) * len(colors) >= BOARD_HEIGHT * BOARD_WIDTH // 2,'There are not sufficient icons'

    board = get_random_board(shape, colors)
    revealed = [[False] * BOARD_WIDTH for i in range(BOARD_HEIGHT)]  # keeps track of visibility of square

    mouse_x = None
    mouse_y = None
    mouse_clicked = False
    first_selection = None

    running = True
    start_game_animation(board)

    while running:
        screen.fill(BGCOLOR)
        draw_board(board, revealed)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = pg.mouse.get_pos()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                mouse_clicked = True

        x, y = get_pos(mouse_x, mouse_y)

        if x is not None and y is not None:
            if not revealed[x][y]:
                if mouse_clicked:
                    revealed[x][y] = True
                    draw_square(board, revealed, x, y)

                    if first_selection is None:
                        first_selection = (x, y)
                    else:
                        pg.time.wait(1000)
                        if board[x][y] != board[first_selection[0]][first_selection[1]]:
                            revealed[x][y] = False
                            revealed[first_selection[0]][first_selection[1]] = False
                        first_selection = None

                    if game_won(revealed):

                        game_won_animation(board, revealed)

                        board = get_random_board(shape, colors)
                        revealed = [[False] * BOARD_WIDTH for i in range(BOARD_HEIGHT)]
                        start_game_animation(board)

                else:
                    draw_select_box(x, y)

        mouse_clicked = False
        pg.display.update()

    else:
       pg.quit()
       quit()
       

if __name__ == '__main__':
    main()