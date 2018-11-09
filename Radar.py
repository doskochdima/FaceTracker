import math
import pygame
import random

screenX = 800
screenY = 450
offset = 50

drawPointX = screenX / 2
drawPointY = screenY - offset

pygame.init()
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("Radar")
font = pygame.font.Font(None, 20)

clock = pygame.time.Clock()


def draw_radar():
    for i in range(100, 301, 100):
        pygame.draw.arc(screen, (0, 255, 0), [drawPointX - i, drawPointY - i, i * 2, i * 2], 0, math.pi, 1)

    for i in range(0, 181, 30):
        x = int(drawPointX + (drawPointX - offset) * math.cos(math.radians(-180 + i)))
        y = int(drawPointY + (drawPointX - offset) * math.sin(math.radians(-180 + i)))
        pygame.draw.line(screen, (0, 255, 0), [drawPointX, drawPointY], [x, y], 1)

    for i in range(0, 181, 30):
        x = int(drawPointX + (drawPointX - offset + 15) * math.cos(math.radians(-180 + i)))
        y = int(drawPointY + (drawPointX - offset + 15) * math.sin(math.radians(-180 + i)))
        screen.blit(font.render(str(i), True, (0, 255, 0)), (x, y))

    pygame.display.flip()


def draw_line():
    for i in range(0, 360, 1):
        clock.tick(100)
        draw_radar()

        x = int(drawPointX + (drawPointX - offset) * math.cos(math.radians(-180 + i * 0.5)))
        y = int(drawPointY + (drawPointX - offset) * math.sin(math.radians(-180 + i * 0.5)))
        pygame.draw.line(screen, (0, 255, 0), [drawPointX, drawPointY], [x, y], 1)

        val = random.randrange(150, 250, 2)
        if (i * 0.5 > 110) and (i * 0.5 < 150):
            x0 = int(drawPointX + val * math.cos(math.radians(-180 + i * 0.5)))
            y0 = int(drawPointY + val * math.sin(math.radians(-180 + i * 0.5)))
            pygame.draw.line(screen, (0, 0, 0), [x0, y0], [x, y], 4)
            pygame.draw.line(screen, (255, 0, 0), [x0, y0], [x, y], 4)

        x = int(drawPointX + (drawPointX - offset) * math.cos(math.radians(-180 + (i - 1) * 0.5)))
        y = int(drawPointY + (drawPointX - offset) * math.sin(math.radians(-180 + (i - 1) * 0.5)))
        pygame.draw.line(screen, (0, 0, 0), [drawPointX, drawPointY], [x, y], 1)

        pygame.display.flip()

    for i in range(360, 0, -1):
        clock.tick(100)
        draw_radar()

        x = int(drawPointX + (drawPointX - offset) * math.cos(math.radians(-180 + i * 0.5)))
        y = int(drawPointY + (drawPointX - offset) * math.sin(math.radians(-180 + i * 0.5)))
        pygame.draw.line(screen, (0, 255, 0), [drawPointX, drawPointY], [x, y], 1)

        val = random.randrange(150, 250, 2)
        if (i * 0.5 > 110) and (i * 0.5 < 150):
            x0 = int(drawPointX + val * math.cos(math.radians(-180 + i * 0.5)))
            y0 = int(drawPointY + val * math.sin(math.radians(-180 + i * 0.5)))
            pygame.draw.line(screen, (0, 0, 0), [x0, y0], [x, y], 4)
            pygame.draw.line(screen, (255, 0, 0), [x0, y0], [x, y], 4)

        x = int(drawPointX + (drawPointX - offset) * math.cos(math.radians(-180 + (i + 1) * 0.5)))
        y = int(drawPointY + (drawPointX - offset) * math.sin(math.radians(-180 + (i + 1) * 0.5)))
        pygame.draw.line(screen, (0, 0, 0), [drawPointX, drawPointY], [x, y], 1)

        pygame.display.flip()


while True:
    draw_line()
