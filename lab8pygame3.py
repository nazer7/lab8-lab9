import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Paint")
screen.fill((255, 255, 255))
pygame.draw.rect(screen, (255,255,255), (0, 0, 600, 60))
colors = {
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'white': (255, 255, 255)
}
color_buttons = []
font = pygame.font.SysFont(None, 24)
x, y = 10, 10
for name, color in colors.items():
    rect = pygame.Rect(x, y, 40, 40)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    color_buttons.append((rect, name))
    x += 45
tools = ['freehand', 'rect', 'circle', 'eraser']
tool_buttons = []
for i, tool in enumerate(tools):
    text = font.render(tool, True, (0, 0, 0))
    rect = pygame.Rect(300 + i*110, 10, 100, 40)
    pygame.draw.rect(screen, (230, 230, 230), rect)
    screen.blit(text, (rect.x + 10, rect.y + 10))
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[1] <60:
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
                if tool == 'rect':
                    rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                    pygame.draw.rect(screen, current_color if tool != 'eraser' else colors['white'], rect, 2)
                elif tool == 'circle':
                    radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                    pygame.draw.circle(screen, current_color if tool != 'eraser' else colors['white'], start_pos, radius, 2)
                drawing = False
    if drawing and tool in ('freehand', 'eraser'):
        mouse_pos = pygame.mouse.get_pos()
        color = current_color if tool != 'eraser' else colors['white']
        if mouse_pos[1] > 60:
            pygame.draw.line(screen, color, last_pos, mouse_pos, 5)
            last_pos = mouse_pos
    pygame.display.update()
    clock.tick(60)

