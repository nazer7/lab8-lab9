import pygame
import sys
import math
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Paint")
screen.fill((255, 255, 255))
colors = {
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'white': (255, 255, 255)
}
#color buttons
color_buttons = []
font = pygame.font.SysFont(None, 24)
x, y = 10, 10
for name, color in colors.items():
    rect = pygame.Rect(x, y, 40, 40)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    color_buttons.append((rect, name))
    x += 45
tools = ['freehand','rect','circle','square','right_triangle','equilateral_triangle','rhombus','eraser']
tool_buttons = []
for i, tool in enumerate(tools):
    text = font.render(tool, True, (0, 0, 0))
    rect = pygame.Rect(10 + i*100, 60, 90, 30)
    pygame.draw.rect(screen, (230, 230, 230), rect)
    screen.blit(text, (rect.x + 5, rect.y + 5))
    tool_buttons.append((rect, tool))
current_color = colors['black']
tool = 'freehand'
drawing = False
start_pos = (0, 0)
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
#mousebutton
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[1] < 100:
 #color button
                for rect, name in color_buttons:
                    if rect.collidepoint(pos):
                        current_color = colors[name]
                for rect, name in tool_buttons:
                    if rect.collidepoint(pos):
                        tool = name
            else:
                drawing = True
                start_pos = pos
                last_pos = pos
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = pygame.mouse.get_pos()
                color = current_color if tool != 'eraser' else colors['white']
                if tool == 'rect':
                    rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                    pygame.draw.rect(screen, color, rect, 2)
                elif tool == 'circle':
                    radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                    pygame.draw.circle(screen, color, start_pos, radius, 2)
                elif tool == 'square':
                    side = min(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    rect = pygame.Rect(start_pos[0], start_pos[1], side, side)
                    pygame.draw.rect(screen, color, rect, 2)
                elif tool == 'right_triangle':
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    pygame.draw.polygon(screen, color, [(x1, y1), (x2, y2), (x1, y2)], 2)
                elif tool == 'equilateral_triangle':
                    x1, y1 = start_pos
                    side = abs(end_pos[0] - x1)
                    height = side * math.sqrt(3) / 2
                    pygame.draw.polygon(screen, color, [
                        (x1, y1),
                        (x1 + side, y1),
                        (x1 + side / 2, y1 - height)  ], 2)
                elif tool == 'rhombus':
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    dx = abs(x2 - x1) // 2
                    dy = abs(y2 - y1) // 2
                    pygame.draw.polygon(screen, color, [
                        (center_x, y1),
                        (x2, center_y),
                        (center_x, y2),
                        (x1, center_y) ], 2)
                drawing = False
#freehand and eraser
    if drawing and tool in ('freehand', 'eraser'):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[1] > 100:
            color = current_color if tool != 'eraser' else colors['white']
            pygame.draw.line(screen, color, last_pos, mouse_pos, 5)
            last_pos = mouse_pos
    pygame.display.update()
    clock.tick(60)
pygame.exit()