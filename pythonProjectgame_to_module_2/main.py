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


def exit_process():
    sys.exit(128)


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
class Button:
    x: int
    y: int
    width: int
    height: int
    caption: str
    procedure: str


@dataclass()
class Event:
    name: str
    state: bool
    processor: str
    counter: int


@dataclass()
class Tile:
    can_walk: bool
    name: str
    id: str
    step_on_text: str
    lookup_text: str
    lookup_event: str


@dataclass()
class Decoration:
    name: str
    id: str
    x: float
    y: float


tiles = [[Tile(True, 'FLOOR', '', '', '', '') for x in range(x_tiles)] for y in range(y_tiles)]
decorations = list()
events = list()


def remove_decoration(decoration_id:str):
    for i in range(len(decorations)):
        if decorations[i].id == decoration_id:
            del decorations[i]
            return


def set_tile_text_by_id(tile_id: str, text: str):
    for iy in range(len(tiles)):
        for ix in range(len(tiles[iy])):
            if tiles[iy][ix].id == tile_id:
                tiles[iy][ix].lookup_text = text


def get_event_state_by_name(name: str) -> bool:
    for e in events:
        if e.name == name:
            return e.state
    return False


def opening_amphora(e: Event):
    e.counter += 1
    for i in range(len(decorations)):
        if decorations[i].id == 'CA1' and e.counter == 2:
            # cast event on decoration
            decorations[i].name = 'OPENED AMPHORA'
            # change tile text, if necessary
            set_tile_text_by_id('CA1', 'Я взял из амфоры нужные продукты. Пора готовить затрак.')
            e.state = True
            return


def breakfast_on_table(e: Event):
    if not get_event_state_by_name('MAKING BREAKFAST'):
        return
    e.counter += 1
    for i in range(len(decorations)):
        if decorations[i].id == 'TB1' and e.counter < 2:
            remove_decoration('FT1')
            decorations.append(Decoration('FOOD ON TABLE', 'FT1', 4.2, 4.85))
            set_tile_text_by_id('TB1', 'Завтрак на столе, можно есть!')
            set_tile_text_by_id('KS1', 'Завтрак на столе.')
            tiles[5][4].lookup_event = 'HAVING BREAKFAST'
            e.state = True
            return


def have_breakfast(e: Event):
    if not get_event_state_by_name('BREAKFAST ON TABLE'):
        return
    e.counter += 1
    for i in range(len(decorations)):
        if decorations[i].id == 'TB1' and e.counter < 2:
            remove_decoration('FT1')
            set_tile_text_by_id('TB1', 'Я съел завтрак, можно спускаться вниз.')
            set_tile_text_by_id('KS1', 'Я уже сготовил и съел завтрак.')
            e.state = True
            return


def make_breakfast(e: Event):
    if not get_event_state_by_name('OPENING AMPHORA'):
        return
    if get_event_state_by_name('BREAKFAST ON TABLE'):
        return
    e.counter += 1
    for i in range(len(decorations)):
        if decorations[i].id == 'KS1' and e.counter < 2:
            decorations.append(Decoration('FOOD ON TABLE', 'FT1', 4.2, 2.55))
            set_tile_text_by_id('KS1', 'Завтрак готов, нужно лишь отнести его на стол.')
            e.state = True


def make_the_bed(e: Event):
    e.counter += 1
    for i in range(len(decorations)):
        if decorations[i].id == 'BD1' and e.counter == 2:
            e.state = True
            set_tile_text_by_id('BD1', 'Кровать опрятно заправлена.')


def execute_event_by_name(name):
    for i in range(len(events)):
        if name == events[i].name:
            prc = events[i].processor + "(events[" + str(i) + "])"
            eval(prc)


def event_by_tile(tile: Tile):
    execute_event_by_name(tile.lookup_event)
    return tile.lookup_text


'''def dialog(screen, font, text_to_show, dialog_x, dialog_y, dialog_w, dialog_h, rect_color):
    draw_text_in_rectangle(screen, font, text_to_show, dialog_x, dialog_y, dialog_w, dialog_h, (255, 255, 255),
                           rect_color)
    while True:
        if pygame.key.get_pressed() == pygame.K_LEFT:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(600, 900, 150, 150))
        if pygame.key.get_pressed() == pygame.K_RIGHT:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(800, 900, 150, 150))
'''


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
    # Stairs
    tiles[3][1].can_walk = True
    tiles[3][1].name = 'STAIRS DOWN'
    tiles[3][1].step_on_text = 'Я не могу уйти, не позавтракав и не заправив кровать.'
    tiles[3][1].lookup_text = 'Эта лестница ведёт на первый этаж. Надо туда спуститься.'
    # Cupboards
    tiles[2][11].can_walk = False
    tiles[2][11].lookup_text = "Шкаф с книгами. Они все хорошие, но сейчас надо идти завтракать."
    decorations.append(Decoration('CUPBOARD WITH BOOKS', 'CB1', 11, 1.8))
    tiles[2][12].can_walk = False
    tiles[2][12].lookup_text = "Я уже оделся, мне тут ничего не нужно."
    decorations.append(Decoration('DRESSER', 'DR1', 12, 1.8))
    tiles[3][6].can_walk = False
    decorations.append(Decoration('CUPBOARD WITH BOTTLES', 'CB4', 6, 2.1))
    tiles[2][10].can_walk = False
    tiles[2][10].lookup_text = "Я уже оделся, мне тут ничего не нужно."
    decorations.append(Decoration('CUPBOARD WITH CLOTHES', 'CB2', 10, 1.7))
    tiles[5][12].can_walk = False
    tiles[6][12].can_walk = False
    tiles[7][12].can_walk = False
    decorations.append(Decoration('SIDE WALL CUPBOARD', 'CB3', 12, 5.3))
    # kitchen set
    tiles[3][3].can_walk = False
    tiles[3][3].lookup_text = ''
    tiles[3][4].can_walk = False
    tiles[3][4].lookup_text = 'Здесь я буду готовить завтрак. Надо только взять продуктов.'
    tiles[3][5].can_walk = False
    tiles[3][5].lookup_text = ''
    decorations.append(Decoration('KITCHEN SET', 'KS1', 3, 2.5))
    # Bed
    decorations.append(Decoration('BED', 'BD1', 8, 2.2))
    tiles[3][8].can_walk = False
    tiles[4][8].can_walk = False
    tiles[3][8].lookup_text = 'Я уже встал, нечего валяться.\n* По кровати разбросаны вещи, её нужно заправить. *'
    decorations.append(Decoration('BEDSIDE TABLE', 'BT1', 8, 4))
    # Windows
    decorations.append(Decoration('EASY WINDOW', 'EW1', 3, 1.25))
    decorations.append(Decoration('EASY WINDOW', 'EW2', 9, 1.25))
    tiles[2][9].lookup_text = 'За окном туман, ничего не видно'
    # Table with food and stools
    tiles[5][4].can_walk = False
    decorations.append(Decoration('TABLE', 'TB1', 4, 5))
    decorations.append(Decoration('STOOL', 'ST1', 3.23, 5.3))
    decorations.append(Decoration('STOOL', 'ST2', 5.23, 5.3))
    # Amphorae
    tiles[7][1].can_walk = False
    tiles[7][2].can_walk = False
    tiles[8][1].can_walk = False
    tiles[8][2].can_walk = False
    tiles[8][3].can_walk = False
    decorations.append(Decoration('CLOSED AMPHORA', 'CA1', 1.15, 7))
    tiles[7][1].lookup_text = 'В этой амфоре есть продукты. Если я хочу позавтракать, нужно её открыть.'
    decorations.append(Decoration('CLOSED AMPHORA', 'CA2', 1.15, 8))
    decorations.append(Decoration('CLOSED AMPHORA', 'CA3', 2.15, 8))
    decorations.append(Decoration('OPENED AMPHORA', 'OA4', 3.15, 8))
    decorations.append(Decoration('OPENED AMPHORA', 'OA5', 2.15, 7))
    # Events in scene
    events.append(Event('OPENING AMPHORA', False, 'opening_amphora', 0))
    tiles[7][1].lookup_event = 'OPENING AMPHORA'
    tiles[7][1].id = 'CA1'
    events.append(Event('MAKING THE BED', False, 'make_the_bed', 0))
    tiles[3][8].lookup_event = 'MAKING THE BED'
    tiles[3][8].id = 'BD1'
    events.append(Event('MAKING BREAKFAST', False, 'make_breakfast', 0))
    tiles[3][4].lookup_event = 'MAKING BREAKFAST'
    tiles[3][4].id = 'KS1'
    events.append(Event('BREAKFAST ON TABLE', False, 'breakfast_on_table', 0))
    tiles[5][4].lookup_event = 'BREAKFAST ON TABLE'
    tiles[5][4].id = 'TB1'
    events.append(Event('HAVING BREAKFAST', False, 'have_breakfast', 0))


def draw_text_in_rectangle(screen, font, text, x, y, w, h, text_color, rect_color):
    # split text0
    lines = text.split("\n")
    # draw rectangle
    pygame.draw.rect(screen, rect_color, pygame.Rect(x, y, w, h))
    for i in range(len(lines)):
        text_width, text_height = font.size(lines[i])
        ts = font.render(lines[i], False, text_color)
        screen.blit(ts, (text_x + 20, text_y + text_height * i))


def main():
    global civ_x, civ_y, civ_dir
    global last_keys
    text_to_show = ''
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    prev_processing_time = datetime.now()
    btns = list()
    btns.append(Button(28, 20, 200, 50, "Exit", "exit_process"))
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
        if keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_DOWN] or keys[
            pygame.K_RETURN]:
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
            elif last_keys[pygame.K_RETURN]:
                if civ_dir == "UP":
                    text_to_show = event_by_tile(tiles[civ_y - 1][civ_x])
                elif civ_dir == "LEFT":
                    text_to_show = event_by_tile(tiles[civ_y][civ_x - 1])
                elif civ_dir == "RIGHT":
                    text_to_show = event_by_tile(tiles[civ_y][civ_x + 1])
                elif civ_dir == "DOWN":
                    text_to_show = event_by_tile(tiles[civ_y + 1][civ_x])
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


init_scene_second_floor()
main()
