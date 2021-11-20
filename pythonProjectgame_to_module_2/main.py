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
cupboard_wbk_image = pygame.image.load('Images/cupboard_with_books.png')
cupboard_wbt_image = pygame.image.load('Images/cupboard_with_bottles.png')
cupboard_wc_image = pygame.image.load('Images/cupboard_with_clothes.png')
dresser_image = pygame.image.load('Images/dresser.png')
sw_cupboard_image = pygame.image.load('Images/side_wall_cupboard.png')
bed_image = pygame.image.load('Images/bed.png')
bedside_table_image = pygame.image.load('Images/bedside_table.png')
civilian_down = pygame.image.load('Images/Civilian01.png')
civilian_left = pygame.image.load('Images/Civilian02.png')
civilian_right = pygame.image.load('Images/Civilian03.png')
civilian_up = pygame.image.load('Images/Civilian04.png')
kitchen_set_image = pygame.image.load('Images/kitchen_set.png')
table_image = pygame.image.load('Images/table.png')
stool_image = pygame.image.load('Images/stool.png')
cl_amphora_image = pygame.image.load('Images/closed_amphora.png')
op_amphora_image = pygame.image.load('Images/opened_amphora.png')
food_on_table_image = pygame.image.load('Images/food_on_table.png')


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
    if name == 'CUPBOARD WITH BOOKS':
        image_to_draw = cupboard_wbk_image
    if name == 'CUPBOARD WITH BOTTLES':
        image_to_draw = cupboard_wbt_image
    if name == 'CUPBOARD WITH CLOTHES':
        image_to_draw = cupboard_wc_image
    if name == 'SIDE WALL CUPBOARD':
        image_to_draw = sw_cupboard_image
    if name == 'DRESSER':
        image_to_draw = dresser_image
    if name == 'EASY WINDOW':
        image_to_draw = easy_window_image
    if name == 'BED':
        image_to_draw = bed_image
    if name == 'BEDSIDE TABLE':
        image_to_draw = bedside_table_image
    if name == 'STAIRS UP':
        image_to_draw = stairs_up_image
    if name == 'STAIRS DOWN':
        image_to_draw = stairs_down_image
    if name == 'KITCHEN SET':
        image_to_draw = kitchen_set_image
    if name == 'TABLE':
        image_to_draw = table_image
    if name == 'STOOL':
        image_to_draw = stool_image
    if name == 'CLOSED AMPHORA':
        image_to_draw = cl_amphora_image
    if name == 'OPENED AMPHORA':
        image_to_draw = op_amphora_image
    if name == 'FOOD ON TABLE':
        image_to_draw = food_on_table_image
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


def init_scene_first_floor():
    global x_tiles, y_tiles
    global civ_x, civ_y
    x_tiles = 36
    y_tiles = 18
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
    # Walls in the middle
    for y in range(y_tiles):
        if 1 <= y < y_tiles - 10:
            tiles[y][x_tiles // 5].can_walk = False
            tiles[y][x_tiles // 5].name = 'UPPER WALL'
        tiles[y_tiles - 10][x_tiles // 5].can_walk = False
        tiles[y_tiles - 10][x_tiles // 5].name = 'WALL UPPER PART'
        tiles[y_tiles - 9][x_tiles // 5].can_walk = False
        tiles[y_tiles - 9][x_tiles // 5].name = 'WALL LOWER PART'

#front walls of 1st room
    tiles[7][8].name = 'UPPER WALL'
    tiles[7][8].can_walk = False
    tiles[8][8].name = 'WALL UPPER PART'
    tiles[8][8].can_walk = False
    tiles[9][8].name = 'WALL LOWER PART'
    tiles[9][8].can_walk = False
    tiles[7][9].name = 'UPPER WALL'
    tiles[7][9].can_walk = False
    tiles[8][9].name = 'WALL UPPER PART'
    tiles[8][9].can_walk = False
    tiles[9][9].name = 'WALL LOWER PART'
    tiles[9][9].can_walk = False
    tiles[7][11].name = 'UPPER WALL'
    tiles[7][11].can_walk = False
    tiles[8][11].name = 'WALL UPPER PART'
    tiles[8][11].can_walk = False
    tiles[9][11].name = 'WALL LOWER PART'
    tiles[9][11].can_walk = False
    tiles[7][12].name = 'UPPER WALL'
    tiles[7][12].can_walk = False
    tiles[8][12].name = 'WALL UPPER PART'
    tiles[8][12].can_walk = False
    tiles[9][12].name = 'WALL LOWER PART'
    tiles[9][12].can_walk = False

    #1st room
    tiles[1][13].name = 'UPPER WALL'
    tiles[1][13].can_walk = False
    tiles[2][13].name = 'UPPER WALL'
    tiles[2][13].can_walk = False
    tiles[3][13].name = 'UPPER WALL'
    tiles[3][13].can_walk = False
    tiles[4][13].name = 'UPPER WALL'
    tiles[4][13].can_walk = False
    tiles[5][13].name = 'UPPER WALL'
    tiles[5][13].can_walk = False
    tiles[6][13].name = 'UPPER WALL'
    tiles[6][13].can_walk = False
    tiles[7][13].name = 'UPPER WALL'
    tiles[7][13].can_walk = False
    tiles[8][13].name = 'WALL UPPER PART'
    tiles[8][13].can_walk = False
    tiles[9][13].name = 'WALL LOWER PART'
    tiles[9][13].can_walk = False

# front walls of 2nd room
    tiles[7][14].name = 'UPPER WALL'
    tiles[7][14].can_walk = False
    tiles[8][14].name = 'WALL UPPER PART'
    tiles[8][14].can_walk = False
    tiles[9][14].name = 'WALL LOWER PART'
    tiles[9][14].can_walk = False
    tiles[8][15].name = 'WALL UPPER PART'
    tiles[8][15].can_walk = False
    tiles[9][15].name = 'WALL LOWER PART'
    tiles[9][15].can_walk = False
    tiles[7][15].name = 'UPPER WALL'
    tiles[7][15].can_walk = False
    tiles[7][17].name = 'UPPER WALL'
    tiles[7][17].can_walk = False
    tiles[8][17].name = 'WALL UPPER PART'
    tiles[8][17].can_walk = False
    tiles[9][17].name = 'WALL LOWER PART'
    tiles[9][17].can_walk = False
    tiles[7][18].name = 'UPPER WALL'
    tiles[7][18].can_walk = False
    tiles[8][18].name = 'WALL UPPER PART'
    tiles[8][18].can_walk = False
    tiles[9][18].name = 'WALL LOWER PART'
    tiles[9][18].can_walk = False


# 2nd room
    tiles[1][19].name = 'UPPER WALL'
    tiles[1][19].can_walk = False
    tiles[2][19].name = 'UPPER WALL'
    tiles[2][19].can_walk = False
    tiles[3][19].name = 'UPPER WALL'
    tiles[3][19].can_walk = False
    tiles[4][19].name = 'UPPER WALL'
    tiles[4][19].can_walk = False
    tiles[5][19].name = 'UPPER WALL'
    tiles[5][19].can_walk = False
    tiles[6][19].name = 'UPPER WALL'
    tiles[6][19].can_walk = False
    tiles[7][19].name = 'UPPER WALL'
    tiles[7][19].can_walk = False
    tiles[8][19].name = 'WALL UPPER PART'
    tiles[8][19].can_walk = False
    tiles[9][19].name = 'WALL LOWER PART'
    tiles[9][19].can_walk = False
# front walls of the 3rd room
    tiles[7][20].name = 'UPPER WALL'
    tiles[7][20].can_walk = False
    tiles[8][20].name = 'WALL UPPER PART'
    tiles[8][20].can_walk = False
    tiles[9][20].name = 'WALL LOWER PART'
    tiles[9][20].can_walk = False
    tiles[7][21].name = 'UPPER WALL'
    tiles[7][21].can_walk = False
    tiles[8][21].name = 'WALL UPPER PART'
    tiles[8][21].can_walk = False
    tiles[9][21].name = 'WALL LOWER PART'
    tiles[9][21].can_walk = False
    tiles[7][23].name = 'UPPER WALL'
    tiles[7][23].can_walk = False
    tiles[8][23].name = 'WALL UPPER PART'
    tiles[8][23].can_walk = False
    tiles[9][23].name = 'WALL LOWER PART'
    tiles[9][23].can_walk = False
    tiles[7][24].name = 'UPPER WALL'
    tiles[7][24].can_walk = False
    tiles[8][24].name = 'WALL UPPER PART'
    tiles[8][24].can_walk = False
    tiles[9][24].name = 'WALL LOWER PART'
    tiles[9][24].can_walk = False

# 3rd room
    tiles[1][25].name = 'UPPER WALL'
    tiles[1][25].can_walk = False
    tiles[2][25].name = 'UPPER WALL'
    tiles[2][25].can_walk = False
    tiles[3][25].name = 'UPPER WALL'
    tiles[3][25].can_walk = False
    tiles[4][25].name = 'UPPER WALL'
    tiles[4][25].can_walk = False
    tiles[5][25].name = 'UPPER WALL'
    tiles[5][25].can_walk = False
    tiles[6][25].name = 'UPPER WALL'
    tiles[6][25].can_walk = False
    tiles[7][25].name = 'UPPER WALL'
    tiles[7][25].can_walk = False
    tiles[8][25].name = 'WALL UPPER PART'
    tiles[8][25].can_walk = False
    tiles[9][25].name = 'WALL LOWER PART'
    tiles[9][25].can_walk = False
# front walls of the 4th room
    tiles[7][26].name = 'UPPER WALL'
    tiles[7][26].can_walk = False
    tiles[8][26].name = 'WALL UPPER PART'
    tiles[8][26].can_walk = False
    tiles[9][26].name = 'WALL LOWER PART'
    tiles[9][26].can_walk = False
    tiles[7][27].name = 'UPPER WALL'
    tiles[7][27].can_walk = False
    tiles[8][27].name = 'WALL UPPER PART'
    tiles[8][27].can_walk = False
    tiles[9][27].name = 'WALL LOWER PART'
    tiles[9][27].can_walk = False
    tiles[7][28].name = 'UPPER WALL'
    tiles[7][28].can_walk = False
    tiles[8][28].name = 'WALL UPPER PART'
    tiles[8][28].can_walk = False
    tiles[9][28].name = 'WALL LOWER PART'
    tiles[9][28].can_walk = False
    tiles[7][29].name = 'UPPER WALL'
    tiles[7][29].can_walk = False
    tiles[8][29].name = 'WALL UPPER PART'
    tiles[8][29].can_walk = False
    tiles[9][29].name = 'WALL LOWER PART'
    tiles[9][29].can_walk = False
    tiles[7][30].name = 'UPPER WALL'
    tiles[7][30].can_walk = False
    tiles[8][30].name = 'WALL UPPER PART'
    tiles[8][30].can_walk = False
    tiles[9][30].name = 'WALL LOWER PART'
    tiles[9][30].can_walk = False
    tiles[7][31].name = 'UPPER WALL'
    tiles[7][31].can_walk = False
    tiles[8][31].name = 'WALL UPPER PART'
    tiles[8][31].can_walk = False
    tiles[9][31].name = 'WALL LOWER PART'
    tiles[9][31].can_walk = False
    tiles[7][33].name = 'UPPER WALL'
    tiles[7][33].can_walk = False
    tiles[8][33].name = 'WALL UPPER PART'
    tiles[8][33].can_walk = False
    tiles[9][33].name = 'WALL LOWER PART'
    tiles[9][33].can_walk = False
    tiles[7][34].name = 'UPPER WALL'
    tiles[7][34].can_walk = False
    tiles[8][34].name = 'WALL UPPER PART'
    tiles[8][34].can_walk = False
    tiles[9][34].name = 'WALL LOWER PART'
    tiles[9][34].can_walk = False
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
init_scene_first_floor()
main()