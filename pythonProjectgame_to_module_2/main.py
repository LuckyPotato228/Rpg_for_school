import pygame
import sys
from dataclasses import dataclass


def process():
    sys.exit(255)


def exit_process():
    sys.exit(128)


@dataclass
class Button:
    x: int
    y: int
    width: int
    height: int
    caption: str
    procedure: str


def main():
    global btns
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    fps = 60
    size = [1920, 1080]
    sky_blue = [135, 206, 250]
    dark_blue = [0, 0, 255]
    black = [0, 0, 0]
    font = pygame.font.SysFont('Comic Sans MS', 27, True)
    buttons = list()
    screen = pygame.display.set_mode(size)
    wall_image = pygame.image.load('Images/wood_wall.png')
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
        pygame.draw.rect(screen, sky_blue, pygame.Rect(0, 768, 1920, 312))
        pygame.draw.rect(screen, dark_blue, pygame.Rect(0, 0, 256, 1080))
        # draw buttons
        for i in range(len(buttons)):
            button = buttons[i]
            pygame.draw.rect(screen, [0, 255, 0], button)
            ts = font.render(btns[i].caption, False, (255, 255, 255))
            screen.blit(ts, (btns[i].x, btns[i].y))
        # draw floor
        for x in range(256, 1920, 32):
            for y in range(0, 768, 32):
                screen.blit(wall_image, pygame.Rect(x, y, wall_image.get_width(), wall_image.get_height()))
        # do other
        pygame.display.update()
        clock.tick(fps)



btns = list()
btns.append(Button(28, 20, 200, 50, "Exit", "process"))
btns.append(Button(28, 100, 200, 50, "Another Exit", "exit_process"))
main()