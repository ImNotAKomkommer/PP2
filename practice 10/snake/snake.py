import pygame
import random
import sys

pygame.init()

# -----------------------------
# Window settings
# -----------------------------
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Practice 10")

clock = pygame.time.Clock()

# -----------------------------
# Colors
# -----------------------------
BLACK = (20, 20, 20)
GREEN = (40, 200, 80)
DARK_GREEN = (20, 130, 60)
RED = (220, 50, 50)
WHITE = (240, 240, 240)
GRAY = (100, 100, 100)
BLUE = (60, 120, 220)
YELLOW = (250, 220, 70)

# -----------------------------
# Fonts
# -----------------------------
font = pygame.font.SysFont("Verdana", 22)
big_font = pygame.font.SysFont("Verdana", 42)

# -----------------------------
# Snake settings
# -----------------------------
snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"
next_direction = "RIGHT"

score = 0
level = 1
speed = 8

# Every 4 foods the level increases
FOODS_PER_LEVEL = 4


def create_walls():
    """
    Creates walls with passages.
    Walls are stored as cell coordinates.
    The passages are empty spaces in the wall.
    """
    walls = []

    # Border walls
    for x in range(0, WIDTH, CELL_SIZE):
        walls.append((x, 0))
        walls.append((x, HEIGHT - CELL_SIZE))

    for y in range(0, HEIGHT, CELL_SIZE):
        walls.append((0, y))
        walls.append((WIDTH - CELL_SIZE, y))

    # Vertical wall with two passages
    vertical_x = WIDTH // 2
    for y in range(80, HEIGHT - 80, CELL_SIZE):
        if y not in range(220, 281, CELL_SIZE) and y not in range(400, 461, CELL_SIZE):
            walls.append((vertical_x, y))

    # Horizontal wall with two passages
    horizontal_y = HEIGHT // 2
    for x in range(80, WIDTH - 80, CELL_SIZE):
        if x not in range(160, 221, CELL_SIZE) and x not in range(380, 441, CELL_SIZE):
            walls.append((x, horizontal_y))

    return walls


walls = create_walls()


def generate_food():
    """
    Generates food in a random position.
    Food must not appear:
    - inside a wall
    - on the snake body
    """
    while True:
        x = random.randrange(CELL_SIZE, WIDTH - CELL_SIZE, CELL_SIZE)
        y = random.randrange(CELL_SIZE, HEIGHT - CELL_SIZE, CELL_SIZE)

        food_position = (x, y)

        if food_position not in snake and food_position not in walls:
            return food_position


food = generate_food()


def draw_grid():
    """Draws a simple grid for better visibility."""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (35, 35, 35), (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (35, 35, 35), (0, y), (WIDTH, y))


def draw_snake():
    """Draws snake body."""
    for index, segment in enumerate(snake):
        rect = pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE)

        if index == 0:
            pygame.draw.rect(screen, YELLOW, rect)
        else:
            pygame.draw.rect(screen, GREEN, rect)

        pygame.draw.rect(screen, DARK_GREEN, rect, 2)


def draw_food():
    """Draws food."""
    rect = pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect, border_radius=6)


def draw_walls():
    """Draws all wall blocks."""
    for wall in walls:
        rect = pygame.Rect(wall[0], wall[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, WHITE, rect, 1)


def show_score_and_level():
    """Displays score and level."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (15, 10))
    screen.blit(level_text, (15, 38))


def game_over():
    """Shows game over screen and exits."""
    screen.fill(BLACK)

    text = big_font.render("GAME OVER", True, RED)
    final_score = font.render(f"Final score: {score}", True, WHITE)
    final_level = font.render(f"Level reached: {level}", True, WHITE)

    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 70))
    screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2))
    screen.blit(final_level, (WIDTH // 2 - final_level.get_width() // 2, HEIGHT // 2 + 35))

    pygame.display.update()
    pygame.time.delay(2500)

    pygame.quit()
    sys.exit()


def update_level():
    """
    Increases level depending on score.
    Every 4 collected foods = next level.
    Speed also increases.
    """
    global level, speed

    new_level = score // FOODS_PER_LEVEL + 1

    if new_level > level:
        level = new_level
        speed += 2


# -----------------------------
# Main game loop
# -----------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Control snake direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                next_direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                next_direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                next_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                next_direction = "RIGHT"

    direction = next_direction

    # Current head position
    head_x, head_y = snake[0]

    # Move head depending on direction
    if direction == "UP":
        head_y -= CELL_SIZE
    elif direction == "DOWN":
        head_y += CELL_SIZE
    elif direction == "LEFT":
        head_x -= CELL_SIZE
    elif direction == "RIGHT":
        head_x += CELL_SIZE

    new_head = (head_x, head_y)

    # -----------------------------
    # Collision checks
    # -----------------------------

    # Check if snake leaves playing area
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        game_over()

    # Check wall collision
    if new_head in walls:
        game_over()

    # Check self collision
    if new_head in snake:
        game_over()

    # Add new head to snake
    snake.insert(0, new_head)

    # Check if food is eaten
    if new_head == food:
        score += 1
        update_level()
        food = generate_food()
    else:
        # If food is not eaten, remove tail
        snake.pop()

    # -----------------------------
    # Drawing
    # -----------------------------
    screen.fill(BLACK)
    draw_grid()
    draw_walls()
    draw_food()
    draw_snake()
    show_score_and_level()

    pygame.display.update()
    clock.tick(speed)