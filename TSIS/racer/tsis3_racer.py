
import pygame
import random
import json
import os
import sys
from datetime import datetime

pygame.init()


# TSIS 3: Racer Game — Advanced Driving, Leaderboard & Power-Ups
# One-file Pygame project.


# Window settings
WIDTH = 700
HEIGHT = 800
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer Game")

clock = pygame.time.Clock()

# Files
LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

# Colors
BLACK = (15, 15, 15)
WHITE = (240, 240, 240)
GRAY = (120, 120, 120)
DARK_GRAY = (45, 45, 45)
LIGHT_GRAY = (180, 180, 180)
GREEN = (40, 150, 70)
ROAD = (50, 50, 50)
ROAD_DARK = (35, 35, 35)
YELLOW = (250, 220, 60)
ORANGE = (255, 150, 30)
RED = (220, 60, 60)
BLUE = (60, 130, 240)
PURPLE = (150, 80, 230)
CYAN = (70, 230, 230)
PINK = (240, 90, 180)

# Fonts
FONT_SMALL = pygame.font.SysFont("Verdana", 16)
FONT = pygame.font.SysFont("Verdana", 22)
FONT_BIG = pygame.font.SysFont("Verdana", 42)
FONT_TITLE = pygame.font.SysFont("Verdana", 52)

# Road settings
ROAD_LEFT = 130
ROAD_RIGHT = 570
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LANES = 3
LANE_WIDTH = ROAD_WIDTH // LANES

FINISH_DISTANCE = 3000

CAR_COLORS = {
    "Blue": BLUE,
    "Red": RED,
    "Yellow": YELLOW,
    "Purple": PURPLE,
    "Cyan": CYAN,
    "Pink": PINK
}

DIFFICULTY_SETTINGS = {
    "Easy": {
        "traffic_spawn": 1.4,
        "obstacle_spawn": 1.8,
        "base_enemy_speed": 4,
        "density_growth": 0.20
    },
    "Normal": {
        "traffic_spawn": 1.0,
        "obstacle_spawn": 1.35,
        "base_enemy_speed": 5,
        "density_growth": 0.30
    },
    "Hard": {
        "traffic_spawn": 0.75,
        "obstacle_spawn": 1.0,
        "base_enemy_speed": 6,
        "density_growth": 0.40
    }
}



# Helper functions for JSON persistence


def load_json(filename, default_data):
    """Loads JSON data from a file. If file does not exist, returns default data."""
    if not os.path.exists(filename):
        return default_data

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return default_data


def save_json(filename, data):
    """Saves data to JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_settings():
    """Loads game settings from settings.json."""
    default_settings = {
        "sound": True,
        "car_color": "Blue",
        "difficulty": "Normal"
    }

    settings = load_json(SETTINGS_FILE, default_settings)

    # Validate loaded settings.
    if settings.get("car_color") not in CAR_COLORS:
        settings["car_color"] = "Blue"

    if settings.get("difficulty") not in DIFFICULTY_SETTINGS:
        settings["difficulty"] = "Normal"

    if not isinstance(settings.get("sound"), bool):
        settings["sound"] = True

    return settings


def load_leaderboard():
    """Loads leaderboard from leaderboard.json."""
    return load_json(LEADERBOARD_FILE, [])


def save_score(name, score, distance, coins):
    """Adds a new score to leaderboard and saves top 10."""
    leaderboard = load_leaderboard()

    entry = {
        "name": name,
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    leaderboard.append(entry)

    # Sort by score first, then by distance.
    leaderboard.sort(key=lambda item: (item["score"], item["distance"]), reverse=True)

    # Keep only top 10.
    leaderboard = leaderboard[:10]

    save_json(LEADERBOARD_FILE, leaderboard)



# UI classes and functions


class Button:
    """Simple Pygame button without external UI libraries."""

    def __init__(self, x, y, w, h, text, color=DARK_GRAY, hover_color=GRAY):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self, surface):
        """Draws the button."""
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        pygame.draw.rect(surface, current_color, self.rect, border_radius=12)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=12)

        text_surface = FONT.render(self.text, True, WHITE)
        surface.blit(
            text_surface,
            (
                self.rect.centerx - text_surface.get_width() // 2,
                self.rect.centery - text_surface.get_height() // 2
            )
        )

    def is_clicked(self, event):
        """Returns True if button is clicked."""
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_center_text(text, font, color, y):
    """Draws centered text at given y coordinate."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y))


def ask_username():
    """Simple username entry screen before starting the game."""
    name = ""
    input_active = True

    while input_active:
        screen.fill(BLACK)
        draw_center_text("Enter your name", FONT_BIG, WHITE, 180)

        input_rect = pygame.Rect(WIDTH // 2 - 160, 300, 320, 50)
        pygame.draw.rect(screen, DARK_GRAY, input_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, input_rect, 2, border_radius=10)

        shown_name = name if name else "Player"
        name_surface = FONT.render(shown_name, True, YELLOW)
        screen.blit(name_surface, (input_rect.x + 15, input_rect.y + 12))

        draw_center_text("Press ENTER to start", FONT, LIGHT_GRAY, 380)
        draw_center_text("Press ESC to return", FONT_SMALL, LIGHT_GRAY, 420)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name.strip() if name.strip() else "Player"

                if event.key == pygame.K_ESCAPE:
                    return None

                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif len(name) < 14 and event.unicode.isprintable():
                    name += event.unicode

        pygame.display.update()
        clock.tick(FPS)



# Game object classes


class PlayerCar:
    """Player car controlled by left and right arrow keys."""

    def __init__(self, color):
        self.width = 48
        self.height = 85
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 130
        self.speed = 7
        self.color = color
        self.base_speed = self.speed

    @property
    def rect(self):
        """Collision rectangle of the player car."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, active_powerup):
        """Updates player movement."""
        keys = pygame.key.get_pressed()

        # Nitro makes horizontal control faster.
        if active_powerup == "Nitro":
            move_speed = self.base_speed + 3
        else:
            move_speed = self.base_speed

        if keys[pygame.K_LEFT] and self.x > ROAD_LEFT + 5:
            self.x -= move_speed

        if keys[pygame.K_RIGHT] and self.x < ROAD_RIGHT - self.width - 5:
            self.x += move_speed

    def draw(self):
        """Draws player car with details."""
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)

        # Windows
        pygame.draw.rect(screen, (180, 220, 255), (self.x + 9, self.y + 12, self.width - 18, 18), border_radius=4)
        pygame.draw.rect(screen, (120, 170, 220), (self.x + 9, self.y + 52, self.width - 18, 18), border_radius=4)

        # Wheels
        pygame.draw.rect(screen, BLACK, (self.x - 6, self.y + 14, 8, 22), border_radius=3)
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 2, self.y + 14, 8, 22), border_radius=3)
        pygame.draw.rect(screen, BLACK, (self.x - 6, self.y + 52, 8, 22), border_radius=3)
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 2, self.y + 52, 8, 22), border_radius=3)

        # Headlights
        pygame.draw.circle(screen, YELLOW, (self.x + 10, self.y + 5), 4)
        pygame.draw.circle(screen, YELLOW, (self.x + self.width - 10, self.y + 5), 4)


class TrafficCar:
    """Enemy traffic car. Collision normally ends the run."""

    def __init__(self, speed):
        self.width = 48
        self.height = 85
        self.lane = random.randint(0, LANES - 1)
        self.x = ROAD_LEFT + self.lane * LANE_WIDTH + LANE_WIDTH // 2 - self.width // 2
        self.y = random.randint(-450, -100)
        self.speed = speed
        self.color = random.choice([RED, ORANGE, PURPLE, CYAN])

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, scroll_speed):
        """Traffic moves downward with track speed."""
        self.y += self.speed + scroll_speed * 0.25

    def draw(self):
        """Draws traffic vehicle."""
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (230, 230, 255), (self.x + 9, self.y + 12, self.width - 18, 18), border_radius=4)
        pygame.draw.rect(screen, (160, 160, 190), (self.x + 9, self.y + 52, self.width - 18, 18), border_radius=4)

        pygame.draw.rect(screen, BLACK, (self.x - 6, self.y + 14, 8, 22), border_radius=3)
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 2, self.y + 14, 8, 22), border_radius=3)
        pygame.draw.rect(screen, BLACK, (self.x - 6, self.y + 52, 8, 22), border_radius=3)
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 2, self.y + 52, 8, 22), border_radius=3)


class Coin:
    """Weighted coin from Practice 11 logic."""

    def __init__(self):
        self.radius = 15
        self.weight = random.choice([1, 1, 1, 2, 2, 3])
        self.lane = random.randint(0, LANES - 1)
        self.x = ROAD_LEFT + self.lane * LANE_WIDTH + LANE_WIDTH // 2
        self.y = random.randint(-600, -80)
        self.speed = 5

    @property
    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self, scroll_speed):
        self.y += self.speed + scroll_speed * 0.15

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius, 3)

        text = FONT_SMALL.render(str(self.weight), True, BLACK)
        screen.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))


class Obstacle:
    """Road obstacle: barrier, oil spill, pothole, speed bump, or moving barrier."""

    def __init__(self, obstacle_type):
        self.type = obstacle_type
        self.lane = random.randint(0, LANES - 1)
        self.width = LANE_WIDTH - 32
        self.height = 32

        if self.type == "barrier":
            self.height = 36
        elif self.type == "oil":
            self.height = 42
        elif self.type == "pothole":
            self.height = 38
        elif self.type == "speed_bump":
            self.height = 24
        elif self.type == "moving_barrier":
            self.height = 32

        self.x = ROAD_LEFT + self.lane * LANE_WIDTH + 16
        self.y = random.randint(-700, -100)
        self.speed = 5

        # Moving barrier shifts horizontally.
        self.move_direction = random.choice([-1, 1])
        self.move_speed = random.uniform(1.2, 2.0)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, scroll_speed):
        self.y += self.speed + scroll_speed * 0.1

        if self.type == "moving_barrier":
            self.x += self.move_direction * self.move_speed

            if self.x < ROAD_LEFT + 5 or self.x + self.width > ROAD_RIGHT - 5:
                self.move_direction *= -1

    def draw(self):
        if self.type == "barrier":
            pygame.draw.rect(screen, RED, self.rect, border_radius=5)
            pygame.draw.line(screen, WHITE, (self.x + 5, self.y + 8), (self.x + self.width - 5, self.y + self.height - 8), 4)
            pygame.draw.line(screen, WHITE, (self.x + 5, self.y + self.height - 8), (self.x + self.width - 5, self.y + 8), 4)

        elif self.type == "oil":
            pygame.draw.ellipse(screen, BLACK, self.rect)
            pygame.draw.ellipse(screen, DARK_GRAY, self.rect, 3)

        elif self.type == "pothole":
            pygame.draw.ellipse(screen, (25, 25, 25), self.rect)
            pygame.draw.ellipse(screen, GRAY, self.rect, 2)

        elif self.type == "speed_bump":
            pygame.draw.rect(screen, YELLOW, self.rect, border_radius=8)
            pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)

        elif self.type == "moving_barrier":
            pygame.draw.rect(screen, ORANGE, self.rect, border_radius=6)
            pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=6)


class PowerUp:
    """Collectible road power-up."""

    def __init__(self, kind):
        self.kind = kind
        self.radius = 18
        self.lane = random.randint(0, LANES - 1)
        self.x = ROAD_LEFT + self.lane * LANE_WIDTH + LANE_WIDTH // 2
        self.y = random.randint(-800, -150)
        self.speed = 5
        self.spawn_time = pygame.time.get_ticks()
        self.timeout = 6000

    @property
    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self, scroll_speed):
        self.y += self.speed + scroll_speed * 0.1

    def expired(self):
        """Power-up disappears if it is not collected quickly enough."""
        return pygame.time.get_ticks() - self.spawn_time >= self.timeout

    def draw(self):
        if self.kind == "Nitro":
            color = CYAN
            label = "N"
        elif self.kind == "Shield":
            color = PURPLE
            label = "S"
        else:
            color = GREEN
            label = "R"

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)

        text = FONT_SMALL.render(label, True, BLACK)
        screen.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))


# Game class


class RacerGame:
    """Main gameplay state."""

    def __init__(self, player_name, settings):
        self.player_name = player_name
        self.settings = settings

        self.difficulty = settings["difficulty"]
        self.diff_data = DIFFICULTY_SETTINGS[self.difficulty]

        self.player = PlayerCar(CAR_COLORS[settings["car_color"]])

        self.traffic = []
        self.obstacles = []
        self.coins = []
        self.powerups = []

        self.score = 0
        self.coins_collected = 0
        self.distance = 0
        self.finished = False

        self.base_scroll_speed = 5
        self.scroll_speed = self.base_scroll_speed
        self.enemy_speed = self.diff_data["base_enemy_speed"]

        self.line_offset = 0

        # Timers are measured in milliseconds.
        now = pygame.time.get_ticks()
        self.last_traffic_spawn = now
        self.last_obstacle_spawn = now
        self.last_coin_spawn = now
        self.last_powerup_spawn = now

        # Active power-up state.
        self.active_powerup = None
        self.powerup_end_time = 0
        self.shield_available = False

        # Repair can restore one crash.
        self.repair_charges = 0

        # Difficulty scaling values.
        self.traffic_interval = self.diff_data["traffic_spawn"] * 1000
        self.obstacle_interval = self.diff_data["obstacle_spawn"] * 1000
        self.coin_interval = 1100
        self.powerup_interval = 6500

        # Used for Practice 11 requirement: enemy speed increases after N coins.
        self.speed_up_every = 8
        self.last_speed_up_coins = 0

        self.game_over = False

    def get_density_multiplier(self):
        """Difficulty scaling based on distance."""
        progress = min(1.0, self.distance / FINISH_DISTANCE)
        growth = self.diff_data["density_growth"]
        return 1.0 + progress * growth

    def safe_lane_far_from_player(self):
        """
        Safe spawn logic.
        It tries not to spawn objects in the same lane directly above the player.
        """
        player_center = self.player.x + self.player.width // 2
        player_lane = int((player_center - ROAD_LEFT) // LANE_WIDTH)
        player_lane = max(0, min(LANES - 1, player_lane))

        possible_lanes = [lane for lane in range(LANES) if lane != player_lane]

        # Sometimes allow same lane, but object is far above screen anyway.
        if random.random() < 0.20:
            possible_lanes.append(player_lane)

        return random.choice(possible_lanes)

    def draw_road(self):
        """Draws arcade road with moving lane lines and checkpoint marks."""
        screen.fill(GREEN)

        # Grass decoration.
        for y in range(0, HEIGHT, 90):
            pygame.draw.rect(screen, (30, 120, 55), (0, y, ROAD_LEFT - 20, 45))
            pygame.draw.rect(screen, (30, 120, 55), (ROAD_RIGHT + 20, y + 25, WIDTH - ROAD_RIGHT, 45))

        # Road shoulders.
        pygame.draw.rect(screen, GRAY, (ROAD_LEFT - 22, 0, 22, HEIGHT))
        pygame.draw.rect(screen, GRAY, (ROAD_RIGHT, 0, 22, HEIGHT))

        # Main road.
        pygame.draw.rect(screen, ROAD, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))
        pygame.draw.rect(screen, ROAD_DARK, (ROAD_LEFT, 0, 8, HEIGHT))
        pygame.draw.rect(screen, ROAD_DARK, (ROAD_RIGHT - 8, 0, 8, HEIGHT))

        # Road borders.
        pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 4)
        pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 4)

        # Moving lane markings.
        self.line_offset += self.scroll_speed
        if self.line_offset > 80:
            self.line_offset = 0

        for lane in range(1, LANES):
            x = ROAD_LEFT + lane * LANE_WIDTH

            for y in range(-80, HEIGHT, 80):
                pygame.draw.rect(screen, WHITE, (x - 3, y + self.line_offset, 6, 45), border_radius=2)

        # Checkpoint strips every 500 meters.
        checkpoint_distance = int(self.distance) % 500
        if checkpoint_distance < 40:
            y = 120
            for x in range(ROAD_LEFT, ROAD_RIGHT, 40):
                color = WHITE if (x // 40) % 2 == 0 else BLACK
                pygame.draw.rect(screen, color, (x, y, 40, 16))

    def spawn_traffic(self):
        """Spawns traffic cars with difficulty scaling."""
        now = pygame.time.get_ticks()
        density = self.get_density_multiplier()
        current_interval = max(420, self.traffic_interval / density)

        if now - self.last_traffic_spawn >= current_interval:
            car = TrafficCar(self.enemy_speed)
            car.lane = self.safe_lane_far_from_player()
            car.x = ROAD_LEFT + car.lane * LANE_WIDTH + LANE_WIDTH // 2 - car.width // 2

            self.traffic.append(car)
            self.last_traffic_spawn = now

    def spawn_obstacle(self):
        """Spawns random road obstacles and dynamic road events."""
        now = pygame.time.get_ticks()
        density = self.get_density_multiplier()
        current_interval = max(450, self.obstacle_interval / density)

        if now - self.last_obstacle_spawn >= current_interval:
            obstacle_type = random.choice([
                "barrier",
                "oil",
                "pothole",
                "speed_bump",
                "moving_barrier"
            ])

            obstacle = Obstacle(obstacle_type)
            obstacle.lane = self.safe_lane_far_from_player()
            obstacle.x = ROAD_LEFT + obstacle.lane * LANE_WIDTH + 16

            self.obstacles.append(obstacle)
            self.last_obstacle_spawn = now

    def spawn_coin(self):
        """Spawns weighted coins."""
        now = pygame.time.get_ticks()

        if now - self.last_coin_spawn >= self.coin_interval:
            coin = Coin()
            coin.lane = random.randint(0, LANES - 1)
            coin.x = ROAD_LEFT + coin.lane * LANE_WIDTH + LANE_WIDTH // 2

            self.coins.append(coin)
            self.last_coin_spawn = now

    def spawn_powerup(self):
        """Spawns power-ups if no active power-up is currently running."""
        now = pygame.time.get_ticks()

        if self.active_powerup is not None:
            return

        if now - self.last_powerup_spawn >= self.powerup_interval:
            kind = random.choice(["Nitro", "Shield", "Repair"])
            powerup = PowerUp(kind)
            powerup.lane = random.randint(0, LANES - 1)
            powerup.x = ROAD_LEFT + powerup.lane * LANE_WIDTH + LANE_WIDTH // 2

            self.powerups.append(powerup)
            self.last_powerup_spawn = now

    def increase_difficulty_if_needed(self):
        """Increases enemy speed after the player collects N coin points."""
        if self.coins_collected - self.last_speed_up_coins >= self.speed_up_every:
            self.enemy_speed += 1
            self.last_speed_up_coins = self.coins_collected

    def activate_powerup(self, kind):
        """
        Activates power-up.
        Only one power-up can be active at a time.
        """
        if self.active_powerup is not None:
            return

        now = pygame.time.get_ticks()

        if kind == "Nitro":
            self.active_powerup = "Nitro"
            self.powerup_end_time = now + 4000
            self.score += 20

        elif kind == "Shield":
            self.active_powerup = "Shield"
            self.shield_available = True
            self.powerup_end_time = 0
            self.score += 15

        elif kind == "Repair":
            # Repair is instant. It gives one repair charge.
            self.active_powerup = "Repair"
            self.repair_charges = 1
            self.powerup_end_time = now + 1000
            self.score += 10

    def update_powerup_state(self):
        """Updates active power-up timer and effects."""
        now = pygame.time.get_ticks()

        if self.active_powerup == "Nitro":
            self.scroll_speed = self.base_scroll_speed + 3

            if now >= self.powerup_end_time:
                self.active_powerup = None
                self.scroll_speed = self.base_scroll_speed

        elif self.active_powerup == "Shield":
            self.scroll_speed = self.base_scroll_speed

        elif self.active_powerup == "Repair":
            self.scroll_speed = self.base_scroll_speed

            if now >= self.powerup_end_time:
                self.active_powerup = None

        else:
            self.scroll_speed = self.base_scroll_speed

    def handle_collision(self, object_to_remove=None):
        """
        Handles dangerous collisions.
        Shield protects from one collision.
        Repair can remove one obstacle or restore one crash.
        """
        if self.active_powerup == "Shield" and self.shield_available:
            self.shield_available = False
            self.active_powerup = None

            if object_to_remove is not None:
                object_to_remove.y = HEIGHT + 100

            return

        if self.repair_charges > 0:
            self.repair_charges -= 1
            self.active_powerup = None

            if object_to_remove is not None:
                object_to_remove.y = HEIGHT + 100

            return

        self.game_over = True

    def update_objects(self):
        """Updates all moving game objects."""
        for car in self.traffic:
            car.update(self.scroll_speed)

        for obstacle in self.obstacles:
            obstacle.update(self.scroll_speed)

        for coin in self.coins:
            coin.update(self.scroll_speed)

        for powerup in self.powerups:
            powerup.update(self.scroll_speed)

        # Remove objects below screen or expired power-ups.
        self.traffic = [car for car in self.traffic if car.y < HEIGHT + 100]
        self.obstacles = [ob for ob in self.obstacles if ob.y < HEIGHT + 100]
        self.coins = [coin for coin in self.coins if coin.y < HEIGHT + 100]
        self.powerups = [
            p for p in self.powerups
            if p.y < HEIGHT + 100 and not p.expired()
        ]

    def check_collisions(self):
        """Checks collisions between player and road objects."""
        player_rect = self.player.rect

        # Traffic collision ends the run unless protected.
        for car in self.traffic:
            if player_rect.colliderect(car.rect):
                self.handle_collision(car)

        # Obstacles have different effects.
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                if obstacle.type in ["barrier", "moving_barrier", "pothole"]:
                    self.handle_collision(obstacle)

                elif obstacle.type == "oil":
                    # Oil spill slows control and gives small penalty.
                    self.player.x += random.choice([-20, 20])
                    self.score = max(0, self.score - 5)
                    obstacle.y = HEIGHT + 100

                elif obstacle.type == "speed_bump":
                    # Speed bump slows progress temporarily.
                    self.distance = max(0, self.distance - 15)
                    obstacle.y = HEIGHT + 100

        # Coin collection.
        for coin in self.coins:
            if player_rect.colliderect(coin.rect):
                self.coins_collected += coin.weight
                self.score += coin.weight * 10
                coin.y = HEIGHT + 100
                self.increase_difficulty_if_needed()

        # Power-up collection.
        for powerup in self.powerups:
            if player_rect.colliderect(powerup.rect):
                self.activate_powerup(powerup.kind)
                powerup.y = HEIGHT + 100

    def update_score_and_distance(self):
        """Calculates distance and distance-based score."""
        self.distance += self.scroll_speed * 0.10

        # Distance score slowly increases.
        self.score += 0.03 * self.scroll_speed

        if self.distance >= FINISH_DISTANCE:
            self.finished = True
            self.score += 500
            self.game_over = True

    def draw_hud(self):
        """Draws score, distance, coins, and active power-up."""
        score_text = FONT.render(f"Score: {int(self.score)}", True, WHITE)
        coins_text = FONT.render(f"Coins: {self.coins_collected}", True, YELLOW)
        distance_left = max(0, FINISH_DISTANCE - int(self.distance))
        distance_text = FONT.render(f"Distance: {int(self.distance)} / {FINISH_DISTANCE}", True, WHITE)
        remaining_text = FONT_SMALL.render(f"Remaining: {distance_left} m", True, LIGHT_GRAY)

        screen.blit(score_text, (15, 15))
        screen.blit(coins_text, (15, 45))
        screen.blit(distance_text, (15, 75))
        screen.blit(remaining_text, (15, 105))

        difficulty_text = FONT_SMALL.render(f"Difficulty: {self.difficulty}", True, WHITE)
        screen.blit(difficulty_text, (WIDTH - difficulty_text.get_width() - 15, 15))

        enemy_text = FONT_SMALL.render(f"Traffic speed: {self.enemy_speed}", True, WHITE)
        screen.blit(enemy_text, (WIDTH - enemy_text.get_width() - 15, 40))

        # Active power-up display.
        if self.active_powerup is None:
            power_text = FONT_SMALL.render("Power-up: none", True, WHITE)

        elif self.active_powerup == "Shield":
            power_text = FONT_SMALL.render("Power-up: Shield active", True, PURPLE)

        else:
            remaining = max(0, (self.powerup_end_time - pygame.time.get_ticks()) // 1000 + 1)
            power_text = FONT_SMALL.render(f"Power-up: {self.active_powerup} ({remaining}s)", True, CYAN)

        screen.blit(power_text, (WIDTH - power_text.get_width() - 15, 65))

        # Finish progress bar.
        bar_x = 15
        bar_y = 135
        bar_w = 220
        bar_h = 14
        progress = min(1.0, self.distance / FINISH_DISTANCE)

        pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_w, bar_h), border_radius=6)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_w * progress), bar_h), border_radius=6)
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 1, border_radius=6)

    def update(self):
        """Runs one frame of gameplay."""
        self.update_powerup_state()
        self.player.update(self.active_powerup)

        self.spawn_traffic()
        self.spawn_obstacle()
        self.spawn_coin()
        self.spawn_powerup()

        self.update_objects()
        self.check_collisions()
        self.update_score_and_distance()

    def draw(self):
        """Draws the full gameplay screen."""
        self.draw_road()

        for coin in self.coins:
            coin.draw()

        for powerup in self.powerups:
            powerup.draw()

        for obstacle in self.obstacles:
            obstacle.draw()

        for car in self.traffic:
            car.draw()

        self.player.draw()
        self.draw_hud()



# Screens


def main_menu(settings):
    """Main Menu screen."""
    play_btn = Button(WIDTH // 2 - 120, 260, 240, 55, "Play")
    leaderboard_btn = Button(WIDTH // 2 - 120, 330, 240, 55, "Leaderboard")
    settings_btn = Button(WIDTH // 2 - 120, 400, 240, 55, "Settings")
    quit_btn = Button(WIDTH // 2 - 120, 470, 240, 55, "Quit")

    while True:
        screen.fill(BLACK)
        draw_center_text("TSIS 3 RACER", FONT_TITLE, YELLOW, 110)
        draw_center_text("Advanced Driving, Leaderboard & Power-Ups", FONT_SMALL, LIGHT_GRAY, 175)

        play_btn.draw(screen)
        leaderboard_btn.draw(screen)
        settings_btn.draw(screen)
        quit_btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if play_btn.is_clicked(event):
                name = ask_username()
                if name is not None:
                    game_loop(name, settings)

            elif leaderboard_btn.is_clicked(event):
                leaderboard_screen()

            elif settings_btn.is_clicked(event):
                settings_screen(settings)

            elif quit_btn.is_clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)


def settings_screen(settings):
    """Settings screen: sound, car color, difficulty."""
    back_btn = Button(WIDTH // 2 - 120, 650, 240, 55, "Back")

    color_names = list(CAR_COLORS.keys())
    difficulty_names = list(DIFFICULTY_SETTINGS.keys())

    while True:
        screen.fill(BLACK)
        draw_center_text("Settings", FONT_BIG, WHITE, 80)

        sound_text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color_text = f"Car Color: {settings['car_color']}"
        difficulty_text = f"Difficulty: {settings['difficulty']}"

        sound_btn = Button(WIDTH // 2 - 160, 200, 320, 50, sound_text)
        color_btn = Button(WIDTH // 2 - 160, 280, 320, 50, color_text)
        difficulty_btn = Button(WIDTH // 2 - 160, 360, 320, 50, difficulty_text)

        sound_btn.draw(screen)
        color_btn.draw(screen)
        difficulty_btn.draw(screen)
        back_btn.draw(screen)

        draw_center_text("Click buttons to change settings", FONT_SMALL, LIGHT_GRAY, 460)
        draw_center_text("Settings are saved to settings.json", FONT_SMALL, LIGHT_GRAY, 490)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_json(SETTINGS_FILE, settings)
                pygame.quit()
                sys.exit()

            if sound_btn.is_clicked(event):
                settings["sound"] = not settings["sound"]
                save_json(SETTINGS_FILE, settings)

            elif color_btn.is_clicked(event):
                index = color_names.index(settings["car_color"])
                settings["car_color"] = color_names[(index + 1) % len(color_names)]
                save_json(SETTINGS_FILE, settings)

            elif difficulty_btn.is_clicked(event):
                index = difficulty_names.index(settings["difficulty"])
                settings["difficulty"] = difficulty_names[(index + 1) % len(difficulty_names)]
                save_json(SETTINGS_FILE, settings)

            elif back_btn.is_clicked(event):
                save_json(SETTINGS_FILE, settings)
                return

        pygame.display.update()
        clock.tick(FPS)


def leaderboard_screen():
    """Displays top 10 leaderboard entries."""
    back_btn = Button(WIDTH // 2 - 120, 700, 240, 55, "Back")

    while True:
        screen.fill(BLACK)
        draw_center_text("Leaderboard - Top 10", FONT_BIG, YELLOW, 60)

        leaderboard = load_leaderboard()

        header = FONT_SMALL.render("Rank   Name           Score     Distance     Coins", True, WHITE)
        screen.blit(header, (85, 145))

        if not leaderboard:
            draw_center_text("No scores yet.", FONT, LIGHT_GRAY, 280)
        else:
            y = 185
            for index, item in enumerate(leaderboard[:10], start=1):
                line = f"{index:<5}  {item['name'][:12]:<12}  {item['score']:<8}  {item['distance']:<10}  {item['coins']}"
                text = FONT_SMALL.render(line, True, WHITE)
                screen.blit(text, (85, y))
                y += 42

        back_btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_btn.is_clicked(event):
                return

        pygame.display.update()
        clock.tick(FPS)


def game_over_screen(game, settings):
    """Game Over screen with Retry and Main Menu buttons."""
    save_score(game.player_name, game.score, game.distance, game.coins_collected)

    retry_btn = Button(WIDTH // 2 - 120, 520, 240, 55, "Retry")
    menu_btn = Button(WIDTH // 2 - 120, 590, 240, 55, "Main Menu")

    while True:
        screen.fill(BLACK)

        title = "FINISH!" if game.finished else "GAME OVER"
        title_color = GREEN if game.finished else RED

        draw_center_text(title, FONT_TITLE, title_color, 120)
        draw_center_text(f"Player: {game.player_name}", FONT, WHITE, 220)
        draw_center_text(f"Score: {int(game.score)}", FONT, YELLOW, 260)
        draw_center_text(f"Distance: {int(game.distance)} m", FONT, WHITE, 300)
        draw_center_text(f"Coins: {game.coins_collected}", FONT, YELLOW, 340)
        draw_center_text(f"Difficulty: {settings['difficulty']}", FONT_SMALL, LIGHT_GRAY, 390)

        retry_btn.draw(screen)
        menu_btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if retry_btn.is_clicked(event):
                game_loop(game.player_name, settings)
                return

            if menu_btn.is_clicked(event):
                return

        pygame.display.update()
        clock.tick(FPS)


def game_loop(player_name, settings):
    """Main game loop."""
    game = RacerGame(player_name, settings)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ESC returns to main menu.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        if not game.game_over:
            game.update()
            game.draw()
        else:
            game_over_screen(game, settings)
            return

        pygame.display.update()
        clock.tick(FPS)



# Program start


def main():
    """Loads settings and opens main menu."""
    settings = load_settings()
    main_menu(settings)


if __name__ == "__main__":
    main()
