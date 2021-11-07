import pygame
import sys
from dataclasses import dataclass
from datetime import datetime

screen_w = 1920
screen_h = 1080
menu_w = 256
text_w = screen_w - menu_w
text_h = 312
text_y = screen_h - text_h
text_x = menu_w
tile_wh = 32
x_tiles = screen_w // tile_wh
y_tiles = screen_h // tile_wh

last_keys = None

wall_image = pygame.image.load('Images/wood_wall.png')
up_wall_image = pygame.image.load('Images/wood_upper_wall.png')
wall_upp_image = pygame.image.load('Images/wood_wall_upper_part.png')
wall_lpp_image = pygame.image.load('Images/wood_wall_lower_part.png')
floor_image = pygame.image.load('Images/wood_floor.png')

def image_by_name(name):
    image_to_draw = floor_image
    if name == 'WALL':
        image_to_draw = wall_image
    if name == 'UPPER WALL':
        image_to_draw = up_wall_image
    if name == 'WALL UPPER PART':
        image_to_draw = wall_upp_image
    if name == 'WALL LOWER PART':
        image_to_draw = wall_lpp_image
    return image_to_draw


@dataclass()
class Tile:
    can_walk: bool
    name: str
    step_on_text: str
    lookup_text: str

@dataclass()
class Decoration:
    name: str
    x: float
    y: float


tiles = [[Tile(True, 'FLOOR', '', '') for x in range(x_tiles)] for y in range(y_tiles)]
decorations = list()


def init_scene_second_floor():
    global x_tiles, y_tiles
    global civ_x, civ_y
    x_tiles = 14
    y_tiles = 12
    civ_x = 2
    civ_y = 3
    for x in range(x_tiles):
        for y in range(y_tiles):
            if x == 0 or x == x_tiles - 1 or y == 0 or y == y_tiles - 3:
                tiles[y][x].can_walk = False
                tiles[y][x].name = 'UPPER WALL'
    for x in range(1, x_tiles - 1):
        tiles[1][x].can_walk = False
        tiles[1][x].name = 'WALL UPPER PART'
        tiles[2][x].can_walk = False
        tiles[2][x].name = 'WALL LOWER PART'
    for x in range(x_tiles):
        tiles[y_tiles - 2][x].can_walk = False
        tiles[y_tiles - 2][x].name = 'WALL UPPER PART'
        tiles[y_tiles - 1][x].can_walk = False
        tiles[y_tiles - 1][x].name = 'WALL LOWER PART'
    # Wall in the middle
    for y in range(y_tiles):
        if 1 <= y < y_tiles - 6:
            tiles[y][x_tiles // 2].can_walk = False
            tiles[y][x_tiles // 2].name = 'UPPER WALL'
        tiles[y_tiles - 6][x_tiles // 2].can_walk = False
        tiles[y_tiles - 6][x_tiles // 2].name = 'WALL UPPER PART'
        tiles[y_tiles - 5][x_tiles // 2].can_walk = False
        tiles[y_tiles - 5][x_tiles // 2].name = 'WALL LOWER PART'
def exit_process():
    sys.exit(128)


@dataclass()
class Button:
    x: int
    y: int
    width: int
    height: int
    caption: str
    procedure: str


def draw_text_in_rectangle(screen, font, text, x, y, w, h, text_col, rect_col):
    # draw rectangle
    pygame.draw.rect(screen, rect_col, pygame.Rect(x, y, w, h))
    text_width, text_height = font.size(text)
    ts = font.render(text, False, text_col)
    screen.blit(ts, (text_x, text_y))


def main():
    global btns
    global civ_x, civ_y, civ_dir
    global last_keys
    text_to_show = ''
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    prev_processing_time = datetime.now()
    fps = 60
    size = [screen_w, screen_h]
    sky_blue = [135, 206, 250]
    dark_blue = [0, 0, 255]
    black = [0, 0, 0]
    font = pygame.font.SysFont('Comic Sans MS', 27, True)
    buttons = list()
    screen = pygame.display.set_mode(size)
    for b in btns:
        buttons.append(pygame.Rect(b.x, b.y, b.width, b.height))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i in range(len(buttons)):
                    if buttons[i].collidepoint(mouse_pos):
                        s = btns[i].procedure + "()"
                        eval(s)
        screen.fill(black)
        # draw menu
        pygame.draw.rect(screen, dark_blue, pygame.Rect(0, 0, menu_w, screen_h))
        # draw buttons
        for i in range(len(buttons)):
            button = buttons[i]
            pygame.draw.rect(screen, [0, 255, 0], button)
            text_width, text_height = font.size(btns[i].caption)
            ts = font.render(btns[i].caption, False, (255, 255, 255))
            screen.blit(ts,
                        (btns[i].x + (button.width - text_width) // 2, btns[i].y + (button.height - text_height) // 2))
        # draw text
        if tiles[civ_y][civ_x].step_on_text != '':
            text_to_show = tiles[civ_y][civ_x].step_on_text
        # draw floor and walls
        x_offset = menu_w + ((screen_w - menu_w) - x_tiles * tile_wh) // 2
        y_offset = ((screen_h - text_h) - y_tiles * tile_wh) // 2
        for x in range(x_tiles):
            for y in range(y_tiles):
                x_coord = x * tile_wh + x_offset
                y_coord = y * tile_wh + y_offset
                image_to_draw = floor_image
                image_to_draw = image_by_name(tiles[y][x].name)
                screen.blit(image_to_draw,
                            pygame.Rect(x_coord, y_coord, image_to_draw.get_width(), image_to_draw.get_height()))
        # show decorations
        for d in decorations:
            x_coord = d.x * tile_wh + x_offset
            y_coord = d.y * tile_wh + y_offset
            image_to_draw = image_by_name(d.name)
            screen.blit(image_to_draw,
                        pygame.Rect(x_coord, y_coord, image_to_draw.get_width(), image_to_draw.get_height()))
        # update screen
        draw_text_in_rectangle(screen, font, text_to_show, text_x, text_y, text_w, text_h, (255, 255, 255), sky_blue)
        pygame.display.update()
        clock.tick(fps)




btns = list()
btns.append(Button(28, 20, 200, 50, "Exit", "exit_process"))
init_scene_second_floor()
main()
