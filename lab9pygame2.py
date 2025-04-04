import pygame
import random
import time
pygame.init()
# create sur
SCREEN_WIDTH=400
SCREEN_HEIGHT=400
SCREEN=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")#name of display sur
WHITE=(255, 255, 255)#colors
GREEN=(0, 255, 0)
RED=(255, 0, 0)
BLACK=(0, 0, 0)
ORANGE=(255, 165, 0)
PURPLE=(128, 0, 128)
BLOCK_SIZE=20 #snake size
FPS=5 #inital snake speed
clock=pygame.time.Clock()
#font for score/level
font=pygame.font.SysFont("Verdana", 20)
score=0 #variable
level=1
speed=FPS
#snake class 
class Snake:
    def __init__(self):
        self.body=[(100, 100), (80, 100), (60, 100)]
        self.direction="RIGHT"
    def move(self):
        head_x, head_y=self.body[0]
        if self.direction == "RIGHT":
            head_x += BLOCK_SIZE
        elif self.direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif self.direction == "UP":
            head_y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            head_y += BLOCK_SIZE
        new_head = (head_x, head_y)
        self.body.insert(0, new_head)
        self.body.pop()
    def grow(self):
        head_x, head_y = self.body[0]
        if self.direction == "RIGHT":
            head_x += BLOCK_SIZE
        elif self.direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif self.direction == "UP":
            head_y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            head_y += BLOCK_SIZE
        new_head = (head_x, head_y)
        self.body.insert(0, new_head)
    def draw(self):
        for segment in self.body:
            pygame.draw.rect(SCREEN, GREEN, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
#food class
class Food:
    def __init__(self, snake_body):
        self.spawn_food(snake_body)
    def spawn_food(self, snake_body):
        self.position = self.random_position(snake_body)
        self.weight = random.randint(1, 3)  # Weight between 1 and 3
        self.timer = time.time()
        self.is_food_on_screen = True
    def random_position(self, snake_body):
        while True:
            x = random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE)
            y = random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE)
            if (x, y) not in snake_body:
                return (x, y)
    def draw(self):
        if self.weight == 1:
            color = RED
        elif self.weight == 2:
            color = ORANGE
        else:
            color = PURPLE
        pygame.draw.rect(SCREEN, color, pygame.Rect(self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))
#display score/level
def show_score(level, score):
    level_text = font.render(f"Level: {level}", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    SCREEN.blit(level_text, [10, 10])
    SCREEN.blit(score_text, [SCREEN_WIDTH - 120, 10])
#border collision
def border_collision(snake_head):
    head_x, head_y = snake_head
    if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
        return True
    return False
# Main game loop
def game_loop():
    global score, level, speed
    snake = Snake()
    food = Food(snake.body)
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"
                elif event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
        snake.move()#snake move
        if border_collision(snake.body[0]):
            game_over = True
        if time.time() - food.timer>8:
            food.spawn_food(snake.body)
#collision with food
        if snake.body[0] == food.position:
            score += food.weight
            snake.grow()
            if score >= level * 3:
                level += 1
                speed += 2
            food.spawn_food(snake.body)
#collision with itself
        if snake.body[0] in snake.body[1:]:
            game_over = True
        SCREEN.fill(WHITE)
        snake.draw()
        food.draw()
        show_score(level, score)
        pygame.display.update()
        clock.tick(speed)
if __name__ == "__main__":
    game_loop()
    pygame.quit()
    exit()
