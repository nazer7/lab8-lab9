import pygame
import random
import time
pygame.init()
# Set up screen dimensions and create display surface
SCREEN_WIDTH=600
SCREEN_HEIGHT=600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
# Snake block size
BLOCK_SIZE = 20
# Set up clock for controlling the snake speed
FPS = 5
clock = pygame.time.Clock()
# Font for score and level
font = pygame.font.SysFont("Verdana", 20)
# Game variables
score = 0
level = 1
speed = FPS
# Snake and food class definitions
class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]  # Initial snake size
        self.direction = "RIGHT"  # Initial snake direction
    def move(self):
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

class Food:
    def __init__(self, snake_body):
        self.position = self.random_position(snake_body)
        self.is_food_on_screen = True

    def random_position(self, snake_body):
        while True:
            x = random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE)
            y = random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE)
            # Ensure food does not appear on the snake's body
            if (x, y) not in snake_body:
                return (x, y)

    def spawn_food(self, snake_body):
        self.position = self.random_position(snake_body)
        self.is_food_on_screen = True

    def draw(self):
        pygame.draw.rect(SCREEN, RED, pygame.Rect(self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# Function to show the score and level
def show_score(level, score):
    level_text = font.render(f"Level: {level}", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    SCREEN.blit(level_text, [10, 10])
    SCREEN.blit(score_text, [SCREEN_WIDTH - 100, 10])

# Function to check for border collision
def check_border_collision(snake_head):
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
        # Handle user input (keypresses)
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

        # Move snake and check for collision with border
        snake.move()
        if check_border_collision(snake.body[0]):
            game_over = True

        # Check for collision with food
        if snake.body[0] == food.position:
            score += 1
            food.is_food_on_screen = False
            snake.grow()
            if score % 3 == 0:  # Every 3 foods increase level and speed
                level += 1
                speed += 2  # Increase speed by 2 FPS
            food.spawn_food(snake.body)

        # Check for self-collision
        if snake.body[0] in snake.body[1:]:
            game_over = True

        # Fill the screen with white and draw snake, food, score, and level
        SCREEN.fill(WHITE)
        snake.draw()
        food.draw()
        show_score(level, score)

        # Update the screen and control the speed
        pygame.display.update()
        clock.tick(speed)
# Start the game loop
if __name__ == "__main__":
    game_loop()
    pygame.quit()
    exit()


