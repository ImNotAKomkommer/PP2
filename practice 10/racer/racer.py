import pygame
import random
import sys

pygame.init()

# Window settings
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer - Practice 10")

clock = pygame.time.Clock()
FPS = 60

# Colors
GREEN = (40, 150, 60)
DARK_GREEN = (25, 110, 45)
ROAD = (45, 45, 45)
ROAD_DARK = (35, 35, 35)
WHITE = (240, 240, 240)
YELLOW = (255, 210, 40)
RED = (200, 40, 40)
BLUE = (50, 120, 230)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
ORANGE = (255, 150, 20)

# Fonts
font = pygame.font.SysFont("Verdana", 24)
big_font = pygame.font.SysFont("Verdana", 42)

# Road settings
ROAD_LEFT = 80
ROAD_RIGHT = 420
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LANE_WIDTH = ROAD_WIDTH // 3

# Player car
player_width = 45
player_height = 80
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 120
player_speed = 6

# Enemy car
enemy_width = 45
enemy_height = 80
enemy_x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - enemy_width - 10)
enemy_y = -enemy_height
enemy_speed = 5

# Coin settings
coin_radius = 13
coin_x = random.randint(ROAD_LEFT + coin_radius, ROAD_RIGHT - coin_radius)
coin_y = random.randint(-500, -50)
coin_speed = 5
coins_collected = 0

# Used for moving dashed road lines
line_offset = 0


def draw_player_car(x, y):
    """Draws player car with simple details."""
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height), border_radius=8)

    # Windshield
    pygame.draw.rect(screen, (170, 220, 255), (x + 8, y + 10, player_width - 16, 18), border_radius=4)

    # Rear window
    pygame.draw.rect(screen, (120, 180, 230), (x + 8, y + 50, player_width - 16, 18), border_radius=4)

    # Wheels
    pygame.draw.rect(screen, BLACK, (x - 6, y + 12, 8, 20), border_radius=3)
    pygame.draw.rect(screen, BLACK, (x + player_width - 2, y + 12, 8, 20), border_radius=3)
    pygame.draw.rect(screen, BLACK, (x - 6, y + 48, 8, 20), border_radius=3)
    pygame.draw.rect(screen, BLACK, (x + player_width - 2, y + 48, 8, 20), border_radius=3)

    # Headlights
    pygame.draw.circle(screen, YELLOW, (x + 10, y + 4), 4)
    pygame.draw.circle(screen, YELLOW, (x + player_width - 10, y + 4), 4)


def draw_enemy_car(x, y):
    """Draws enemy car with simple details."""
    pygame.draw.rect(screen, RED, (x, y, enemy_width, enemy_height), border_radius=8)

    # Windows
    pygame.draw.rect(screen, (230, 180, 180), (x + 8, y + 10, enemy_width - 16, 18), border_radius=4)
    pygame.draw.rect(screen, (180, 120, 120), (x + 8, y + 50, enemy_width - 16, 18), border_radius=4)

    # Wheels
    pygame.draw.rect(screen, BLACK, (x - 6, y + 12, 8, 20), border_radius=3)
    pygame.draw.rect(screen, BLACK, (x + enemy_width - 2, y + 12, 8, 20), border_radius=3)
    pygame.draw.rect(screen, BLACK, (x - 6, y + 48, 8, 20), border_radius=3)
    pygame.draw.rect(screen, BLACK, (x + enemy_width - 2, y + 48, 8, 20), border_radius=3)


def draw_road():
    """Draws a more detailed road with three lanes and shoulders."""
    global line_offset

    # Grass background
    screen.fill(GREEN)

    # Add darker grass stripes
    for i in range(0, HEIGHT, 80):
        pygame.draw.rect(screen, DARK_GREEN, (0, i, ROAD_LEFT, 40))
        pygame.draw.rect(screen, DARK_GREEN, (ROAD_RIGHT, i + 20, WIDTH - ROAD_RIGHT, 40))

    # Road shoulder
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT - 18, 0, 18, HEIGHT))
    pygame.draw.rect(screen, GRAY, (ROAD_RIGHT, 0, 18, HEIGHT))

    # Main road
    pygame.draw.rect(screen, ROAD, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

    # Slight darker side parts of the road
    pygame.draw.rect(screen, ROAD_DARK, (ROAD_LEFT, 0, 8, HEIGHT))
    pygame.draw.rect(screen, ROAD_DARK, (ROAD_RIGHT - 8, 0, 8, HEIGHT))

    # Road borders
    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 4)

    # Moving dashed lane lines
    line_offset += enemy_speed
    if line_offset > 50:
        line_offset = 0

    lane1_x = ROAD_LEFT + LANE_WIDTH
    lane2_x = ROAD_LEFT + LANE_WIDTH * 2

    for y in range(-50, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (lane1_x - 3, y + line_offset, 6, 45), border_radius=2)
        pygame.draw.rect(screen, WHITE, (lane2_x - 3, y + line_offset, 6, 45), border_radius=2)


def draw_coin(x, y):
    """Draws a coin."""
    pygame.draw.circle(screen, YELLOW, (x, y), coin_radius)
    pygame.draw.circle(screen, ORANGE, (x, y), coin_radius, 3)
    pygame.draw.circle(screen, (255, 240, 120), (x - 4, y - 4), 4)


def reset_enemy():
    """Places enemy car back above the screen."""
    global enemy_x, enemy_y
    enemy_x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - enemy_width - 10)
    enemy_y = random.randint(-300, -100)


def reset_coin():
    """Places coin back above the screen, inside the road."""
    global coin_x, coin_y
    coin_x = random.randint(ROAD_LEFT + coin_radius + 5, ROAD_RIGHT - coin_radius - 5)
    coin_y = random.randint(-500, -50)


def game_over():
    """Shows game over screen and exits."""
    text = big_font.render("GAME OVER", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 40))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x > ROAD_LEFT + 5:
        player_x -= player_speed

    if keys[pygame.K_RIGHT] and player_x < ROAD_RIGHT - player_width - 5:
        player_x += player_speed

    # Move enemy and coin down
    enemy_y += enemy_speed
    coin_y += coin_speed

    # Reset enemy if it leaves screen
    if enemy_y > HEIGHT:
        reset_enemy()

    # Reset coin if it leaves screen
    if coin_y > HEIGHT:
        reset_coin()

    # Rectangles for collision detection
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    coin_rect = pygame.Rect(coin_x - coin_radius, coin_y - coin_radius, coin_radius * 2, coin_radius * 2)

    # Collision with enemy
    if player_rect.colliderect(enemy_rect):
        game_over()

    # Collect coin
    if player_rect.colliderect(coin_rect):
        coins_collected += 1
        reset_coin()

    # Draw everything
    draw_road()
    draw_coin(coin_x, coin_y)
    draw_enemy_car(enemy_x, enemy_y)
    draw_player_car(player_x, player_y)

    # Coin counter in top right corner
    coin_text = font.render(f"Coins: {coins_collected}", True, YELLOW)
    screen.blit(coin_text, (WIDTH - coin_text.get_width() - 15, 15))

    pygame.display.update()
    clock.tick(FPS)