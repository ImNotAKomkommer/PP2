import pygame
import random
import sys

pygame.init()

# Window settings
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer - Practice 11")

clock = pygame.time.Clock()
FPS = 60

# Colors
GREEN = (40, 150, 60)
ROAD = (45, 45, 45)
WHITE = (240, 240, 240)
YELLOW = (255, 220, 40)
ORANGE = (255, 140, 20)
BLUE = (50, 120, 230)
RED = (210, 50, 50)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)

# Fonts
font = pygame.font.SysFont("Verdana", 24)
small_font = pygame.font.SysFont("Verdana", 16)
big_font = pygame.font.SysFont("Verdana", 42)

# Road settings
ROAD_LEFT = 80
ROAD_RIGHT = 420
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

# Player settings
player_width = 45
player_height = 80
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 120
player_speed = 6

# Enemy settings
enemy_width = 45
enemy_height = 80
enemy_x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - enemy_width - 10)
enemy_y = -enemy_height
enemy_speed = 5

# Enemy speed increases every N coin points
SPEED_UP_EVERY = 5
last_speed_up_score = 0

# Coin settings
coin_radius = 15
coin_x = 0
coin_y = 0
coin_weight = 1
coin_speed = 5

score = 0

# Used for moving road lines
line_offset = 0


def reset_coin():
    """
    Creates a new coin above the screen.
    Coin has random weight.
    Higher weight gives more score.
    """
    global coin_x, coin_y, coin_weight

    coin_x = random.randint(ROAD_LEFT + coin_radius, ROAD_RIGHT - coin_radius)
    coin_y = random.randint(-500, -50)

    # Different coin weights.
    # Most coins are weight 1, rarer coins are weight 2 or 3.
    coin_weight = random.choice([1, 1, 1, 2, 2, 3])


def reset_enemy():
    """Places enemy car above the screen."""
    global enemy_x, enemy_y

    enemy_x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - enemy_width - 10)
    enemy_y = random.randint(-300, -100)


def draw_road():
    """Draws road with three lanes and side borders."""
    global line_offset

    screen.fill(GREEN)

    # Side shoulders
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT - 20, 0, 20, HEIGHT))
    pygame.draw.rect(screen, GRAY, (ROAD_RIGHT, 0, 20, HEIGHT))

    # Main road
    pygame.draw.rect(screen, ROAD, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

    # Road borders
    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 4)

    # Moving dashed lane lines
    line_offset += enemy_speed
    if line_offset > 80:
        line_offset = 0

    lane_1 = ROAD_LEFT + ROAD_WIDTH // 3
    lane_2 = ROAD_LEFT + ROAD_WIDTH // 3 * 2

    for y in range(-80, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (lane_1 - 3, y + line_offset, 6, 45))
        pygame.draw.rect(screen, WHITE, (lane_2 - 3, y + line_offset, 6, 45))


def draw_player_car(x, y):
    """Draws player car."""
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height), border_radius=8)

    # Windows
    pygame.draw.rect(screen, (170, 220, 255), (x + 8, y + 10, player_width - 16, 18), border_radius=4)
    pygame.draw.rect(screen, (120, 180, 230), (x + 8, y + 50, player_width - 16, 18), border_radius=4)

    # Wheels
    pygame.draw.rect(screen, BLACK, (x - 5, y + 12, 7, 20))
    pygame.draw.rect(screen, BLACK, (x + player_width - 2, y + 12, 7, 20))
    pygame.draw.rect(screen, BLACK, (x - 5, y + 48, 7, 20))
    pygame.draw.rect(screen, BLACK, (x + player_width - 2, y + 48, 7, 20))


def draw_enemy_car(x, y):
    """Draws enemy car."""
    pygame.draw.rect(screen, RED, (x, y, enemy_width, enemy_height), border_radius=8)

    # Windows
    pygame.draw.rect(screen, (240, 180, 180), (x + 8, y + 10, enemy_width - 16, 18), border_radius=4)
    pygame.draw.rect(screen, (180, 100, 100), (x + 8, y + 50, enemy_width - 16, 18), border_radius=4)

    # Wheels
    pygame.draw.rect(screen, BLACK, (x - 5, y + 12, 7, 20))
    pygame.draw.rect(screen, BLACK, (x + enemy_width - 2, y + 12, 7, 20))
    pygame.draw.rect(screen, BLACK, (x - 5, y + 48, 7, 20))
    pygame.draw.rect(screen, BLACK, (x + enemy_width - 2, y + 48, 7, 20))


def draw_coin():
    """Draws coin and shows its weight."""
    pygame.draw.circle(screen, YELLOW, (coin_x, coin_y), coin_radius)
    pygame.draw.circle(screen, ORANGE, (coin_x, coin_y), coin_radius, 3)

    weight_text = small_font.render(str(coin_weight), True, BLACK)
    screen.blit(
        weight_text,
        (
            coin_x - weight_text.get_width() // 2,
            coin_y - weight_text.get_height() // 2
        )
    )


def increase_enemy_speed_if_needed():
    """
    Increases enemy speed when the player earns enough coin points.
    Example: every 5 points enemy becomes faster.
    """
    global enemy_speed, last_speed_up_score

    if score - last_speed_up_score >= SPEED_UP_EVERY:
        enemy_speed += 1
        last_speed_up_score = score


def game_over():
    """Shows game over screen."""
    text = big_font.render("GAME OVER", True, RED)
    final_score = font.render(f"Coins: {score}", True, WHITE)

    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.update()
    pygame.time.delay(2500)

    pygame.quit()
    sys.exit()


# Create first coin
reset_coin()

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

    # Move enemy and coin
    enemy_y += enemy_speed
    coin_y += coin_speed

    # Reset objects when they leave the screen
    if enemy_y > HEIGHT:
        reset_enemy()

    if coin_y > HEIGHT:
        reset_coin()

    # Collision rectangles
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    coin_rect = pygame.Rect(
        coin_x - coin_radius,
        coin_y - coin_radius,
        coin_radius * 2,
        coin_radius * 2
    )

    # Enemy collision
    if player_rect.colliderect(enemy_rect):
        game_over()

    # Coin collision
    if player_rect.colliderect(coin_rect):
        score += coin_weight
        increase_enemy_speed_if_needed()
        reset_coin()

    # Draw everything
    draw_road()
    draw_coin()
    draw_enemy_car(enemy_x, enemy_y)
    draw_player_car(player_x, player_y)

    # Score in the top right corner
    score_text = font.render(f"Coins: {score}", True, YELLOW)
    speed_text = small_font.render(f"Enemy speed: {enemy_speed}", True, WHITE)

    screen.blit(score_text, (WIDTH - score_text.get_width() - 15, 15))
    screen.blit(speed_text, (WIDTH - speed_text.get_width() - 15, 45))

    pygame.display.update()
    clock.tick(FPS)