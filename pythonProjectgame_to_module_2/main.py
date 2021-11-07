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
civ_x = 2
civ_y = 2
civ_dir = "DOWN"  # DOWN, UP, LEFT, RIGHT
tile_wh = 32
x_tiles = screen_w // tile_wh
y_tiles = screen_h // tile_wh

last_keys = None

stairs_up_image = pygame.image.load('Images/stone_stairs_up.png')
stairs_down_image = pygame.image.load('Images/stone_stairs_down.png')
wall_image = pygame.image.load('Images/wood_wall.png')
easy_window_image = pygame.image.load('Images/wood_window.png')
up_wall_image = pygame.image.load('Images/wood_upper_wall.png')
wall_upp_image = pygame.image.load('Images/wood_wall_upper_part.png')
wall_lpp_image = pygame.image.load('Images/wood_wall_lower_part.png')
floor_image = pygame.image.load('Images/wood_floor.png')
civilian_down = pygame.image.load('Images/Civilian01.png')
civilian_left = pygame.image.load('Images/Civilian02.png')
civilian_right = pygame.image.load('Images/Civilian03.png')
civilian_up = pygame.image.load('Images/Civilian04.png')

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
        # do civilian moves
        this_processing_time = datetime.now()
        time_diff = (this_processing_time - prev_processing_time).total_seconds() * 1000
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_DOWN] or keys[pygame.K_SPACE]:
            if time_diff >= 100:
                last_keys = keys
        # process keystrokes
        if last_keys is not None and time_diff >= 250:
            text_to_show = ''
            if last_keys[pygame.K_UP]:
                if tiles[civ_y - 1][civ_x].can_walk:
                    civ_y -= 1
                civ_dir = "UP"
            elif last_keys[pygame.K_LEFT]:
                if tiles[civ_y][civ_x - 1].can_walk:
                    civ_x -= 1
                civ_dir = "LEFT"
            elif last_keys[pygame.K_RIGHT]:
                if tiles[civ_y][civ_x + 1].can_walk:
                    civ_x += 1
                civ_dir = "RIGHT"
            elif last_keys[pygame.K_DOWN]:
                if tiles[civ_y + 1][civ_x].can_walk:
                    civ_y += 1
                civ_dir = "DOWN"
            elif last_keys[pygame.K_SPACE]:
                if civ_dir == "UP":
                    text_to_show = tiles[civ_y-1][civ_x].lookup_text
                elif civ_dir == "LEFT":
                    text_to_show = tiles[civ_y][civ_x-1].lookup_text
                elif civ_dir == "RIGHT":
                    text_to_show = tiles[civ_y][civ_x+1].lookup_text
                elif civ_dir == "DOWN":
                    text_to_show = tiles[civ_x][civ_y+1].lookup_text
            prev_processing_time = this_processing_time
            last_keys = None
        # render civilian
        civ_picture = civilian_down
        if civ_dir == "DOWN":
            civ_picture = civilian_down
        elif civ_dir == "UP":
            civ_picture = civilian_up
        elif civ_dir == "LEFT":
            civ_picture = civilian_left
        elif civ_dir == "RIGHT":
            civ_picture = civilian_right
        screen.blit(civ_picture,
                    pygame.Rect(civ_x * tile_wh + x_offset, civ_y * tile_wh + y_offset, civilian_down.get_width(),
                                civilian_down.get_height()))
        # update screen
        draw_text_in_rectangle(screen, font, text_to_show, text_x, text_y, text_w, text_h, (255, 255, 255), sky_blue)
        pygame.display.update()
        clock.tick(fps)


# pygame.quit()
# sys.exit


btns = list()
btns.append(Button(28, 20, 200, 50, "Exit", "exit_process"))
init_scene_second_floor()
main()
