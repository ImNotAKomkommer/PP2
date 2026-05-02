import pygame
import random
import sys

pygame.init()

# Window settings
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Practice 11")

clock = pygame.time.Clock()

# Colors
BLACK = (20, 20, 20)
GREEN = (50, 200, 80)
DARK_GREEN = (20, 120, 50)
RED = (220, 50, 50)
YELLOW = (250, 220, 60)
BLUE = (70, 130, 240)
WHITE = (240, 240, 240)
GRAY = (80, 80, 80)

# Fonts
font = pygame.font.SysFont("Verdana", 22)
small_font = pygame.font.SysFont("Verdana", 16)
big_font = pygame.font.SysFont("Verdana", 42)

# Snake settings
snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"
next_direction = "RIGHT"

score = 0
speed = 8

# Food settings
food = None
food_weight = 1

# Food disappears after 5 seconds
FOOD_LIFETIME = 5000
food_spawn_time = 0


def create_walls():
    """
    Creates inner walls with passages.
    The snake dies if it touches a wall.
    """
    walls = []

    # Vertical wall with passages
    wall_x = WIDTH // 2

    for y in range(80, HEIGHT - 80, CELL_SIZE):
        # Passages in the wall
        if y not in range(220, 281, CELL_SIZE) and y not in range(400, 461, CELL_SIZE):
            walls.append((wall_x, y))

    # Horizontal wall with passages
    wall_y = HEIGHT // 2

    for x in range(80, WIDTH - 80, CELL_SIZE):
        # Passages in the wall
        if x not in range(160, 221, CELL_SIZE) and x not in range(380, 441, CELL_SIZE):
            walls.append((x, wall_y))

    return walls


walls = create_walls()


def generate_food():
    """
    Generates food at a random position.
    Food cannot appear on the snake or inside walls.
    Food has different weights.
    """
    global food, food_weight, food_spawn_time

    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)

        new_food = (x, y)

        # Food must not spawn on snake or wall
        if new_food not in snake and new_food not in walls:
            food = new_food

            # Different food weights
            food_weight = random.choice([1, 1, 1, 2, 2, 3])

            # Save spawn time for timer
            food_spawn_time = pygame.time.get_ticks()
            break


def draw_grid():
    """Draws background grid."""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (35, 35, 35), (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (35, 35, 35), (0, y), (WIDTH, y))


def draw_walls():
    """Draws all wall blocks."""
    for wall in walls:
        rect = pygame.Rect(wall[0], wall[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, WHITE, rect, 1)


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
    """Draws food and shows its weight."""
    rect = pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE)

    if food_weight == 1:
        color = RED
    elif food_weight == 2:
        color = BLUE
    else:
        color = YELLOW

    pygame.draw.rect(screen, color, rect, border_radius=5)

    weight_text = small_font.render(str(food_weight), True, BLACK)
    screen.blit(
        weight_text,
        (
            food[0] + CELL_SIZE // 2 - weight_text.get_width() // 2,
            food[1] + CELL_SIZE // 2 - weight_text.get_height() // 2
        )
    )


def draw_info():
    """Shows score, food weight, and timer."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (15, 10))

    elapsed_time = pygame.time.get_ticks() - food_spawn_time
    remaining_time = max(0, (FOOD_LIFETIME - elapsed_time) // 1000 + 1)

    timer_text = font.render(f"Food time: {remaining_time}", True, WHITE)
    screen.blit(timer_text, (15, 40))

    weight_text = font.render(f"Food weight: {food_weight}", True, WHITE)
    screen.blit(weight_text, (15, 70))


def check_food_timer():
    """
    If food exists for too long, it disappears.
    Then a new food is generated.
    """
    current_time = pygame.time.get_ticks()

    if current_time - food_spawn_time >= FOOD_LIFETIME:
        generate_food()


def game_over():
    """Shows game over screen and exits the game."""
    screen.fill(BLACK)

    text = big_font.render("GAME OVER", True, RED)
    final_score = font.render(f"Final score: {score}", True, WHITE)

    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.update()
    pygame.time.delay(2500)

    pygame.quit()
    sys.exit()


# Generate first food
generate_food()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Snake direction control
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

    # Current snake head
    head_x, head_y = snake[0]

    # Move snake head
    if direction == "UP":
        head_y -= CELL_SIZE
    elif direction == "DOWN":
        head_y += CELL_SIZE
    elif direction == "LEFT":
        head_x -= CELL_SIZE
    elif direction == "RIGHT":
        head_x += CELL_SIZE

    new_head = (head_x, head_y)

    # Check border collision
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        game_over()

    # Check wall collision
    if new_head in walls:
        game_over()

    # Check self collision
    if new_head in snake:
        game_over()

    # Add new head
    snake.insert(0, new_head)

    # Check food collision
    if new_head == food:
        score += food_weight
        generate_food()
    else:
        snake.pop()

    # Check if food should disappear
    check_food_timer()

    # Draw everything
    screen.fill(BLACK)
    draw_grid()
    draw_walls()
    draw_food()
    draw_snake()
    draw_info()

    pygame.display.update()
    clock.tick(speed)