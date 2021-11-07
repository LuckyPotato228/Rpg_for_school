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
    size = [800, 600]
    black = [135, 206, 250]
    font = pygame.font.SysFont('Comic Sans MS', 27, True)
    data = 'Exit'
    ts = font.render(data,False,(255,255,255))
    buttons = list()
    screen = pygame.display.set_mode(size)
    for b in btns:
        buttons.append(pygame.Rect(b.x, b.y, b.width, b.height))
    screen.fill(black)
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
        for i in range(len(buttons)):
            button = buttons[i]
            pygame.draw.rect(screen, [0, 255, 0], button)
            ts = font.render(btns[i].caption, False, (255, 255, 255))
            screen.blit( ts, (btns[i].x, btns[i].y))
        pygame.display.update()
        clock.tick(fps)


btns = list()
btns.append(Button(200, 200, 500, 250, "Fine Button", "process"))
btns.append(Button(20, 40, 100, 50, "more buttons", "exit_process"))
main()