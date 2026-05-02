# TSIS 4 Snake Game 
# Uses only pygame, psycopg2, json, random, sys, os.

import pygame
import random
import sys
import json
import os

from db import Database


pygame.init()

# Window settings
WIDTH = 720
HEIGHT = 720
CELL_SIZE = 24
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4 Snake Game")

clock = pygame.time.Clock()

# Files
SETTINGS_FILE = "settings.json"

# Colors
BLACK = (18, 18, 18)
WHITE = (240, 240, 240)
GRAY = (90, 90, 90)
DARK_GRAY = (45, 45, 45)
LIGHT_GRAY = (170, 170, 170)
GREEN = (60, 210, 90)
DARK_GREEN = (20, 130, 60)
RED = (230, 55, 55)
DARK_RED = (120, 0, 0)
YELLOW = (250, 220, 70)
BLUE = (70, 140, 240)
CYAN = (70, 230, 230)
PURPLE = (160, 90, 240)
ORANGE = (255, 150, 40)

# Fonts
FONT_SMALL = pygame.font.SysFont("Verdana", 16)
FONT = pygame.font.SysFont("Verdana", 22)
FONT_BIG = pygame.font.SysFont("Verdana", 42)
FONT_TITLE = pygame.font.SysFont("Verdana", 52)

# Gameplay constants
FOOD_LIFETIME = 5000
POISON_LIFETIME = 7000
POWERUP_FIELD_LIFETIME = 8000
POWERUP_EFFECT_DURATION = 5000

FOODS_PER_LEVEL = 4
BASE_SPEED = 8


# ============================================================
# JSON settings
# ============================================================

def load_settings():
    """Loads settings from settings.json."""
    default_settings = {
        "snake_color": [60, 210, 90],
        "grid": True,
        "sound": True
    }

    if not os.path.exists(SETTINGS_FILE):
        save_settings(default_settings)
        return default_settings

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)

        if "snake_color" not in settings:
            settings["snake_color"] = default_settings["snake_color"]

        if "grid" not in settings:
            settings["grid"] = default_settings["grid"]

        if "sound" not in settings:
            settings["sound"] = default_settings["sound"]

        return settings

    except Exception:
        return default_settings


def save_settings(settings):
    """Saves settings to settings.json."""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


# ============================================================
# Basic UI
# ============================================================

class Button:
    """Simple button made with Pygame rectangles."""

    def __init__(self, x, y, w, h, text, color=DARK_GRAY, hover_color=GRAY):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        pygame.draw.rect(screen, current_color, self.rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=12)

        text_surface = FONT.render(self.text, True, WHITE)
        screen.blit(
            text_surface,
            (
                self.rect.centerx - text_surface.get_width() // 2,
                self.rect.centery - text_surface.get_height() // 2
            )
        )

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_center_text(text, font, color, y):
    """Draws centered text."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y))


def username_input_screen():
    """Screen where player types username using keyboard."""
    username = ""

    while True:
        screen.fill(BLACK)

        draw_center_text("Enter username", FONT_BIG, WHITE, 170)

        input_rect = pygame.Rect(WIDTH // 2 - 180, 300, 360, 55)
        pygame.draw.rect(screen, DARK_GRAY, input_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, input_rect, 2, border_radius=10)

        shown_text = username if username else "Player"
        text_surface = FONT.render(shown_text, True, YELLOW)
        screen.blit(text_surface, (input_rect.x + 15, input_rect.y + 13))

        draw_center_text("Press ENTER to play", FONT, LIGHT_GRAY, 390)
        draw_center_text("Press ESC to return", FONT_SMALL, LIGHT_GRAY, 430)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return username.strip() if username.strip() else "Player"

                if event.key == pygame.K_ESCAPE:
                    return None

                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif len(username) < 16 and event.unicode.isprintable():
                    username += event.unicode

        pygame.display.update()
        clock.tick(FPS)


# ============================================================
# Snake Game
# ============================================================

class SnakeGame:
    """Main Snake game class."""

    def __init__(self, username, settings, database):
        self.username = username
        self.settings = settings
        self.database = database

        self.snake_color = tuple(settings["snake_color"])
        self.show_grid = settings["grid"]

        # Snake body is a list of cell coordinates.
        self.snake = [
            (CELL_SIZE * 5, CELL_SIZE * 5),
            (CELL_SIZE * 4, CELL_SIZE * 5),
            (CELL_SIZE * 3, CELL_SIZE * 5)
        ]

        self.direction = "RIGHT"
        self.next_direction = "RIGHT"

        self.score = 0
        self.foods_eaten = 0
        self.level = 1
        self.base_speed = BASE_SPEED
        self.current_speed = BASE_SPEED

        self.personal_best = database.get_personal_best(username)

        # Food state.
        self.food = None
        self.food_weight = 1
        self.food_spawn_time = 0

        # Poison food state.
        self.poison_food = None
        self.poison_spawn_time = 0

        # Power-up state.
        self.powerup = None
        self.powerup_type = None
        self.powerup_spawn_time = 0

        self.active_powerup = None
        self.powerup_end_time = 0
        self.shield_ready = False

        # Obstacles appear from level 3.
        self.obstacles = []

        self.game_over = False
        self.saved = False

        self.generate_food()
        self.generate_poison_food()

    def cell_positions(self):
        """Returns all valid grid cells."""
        positions = []

        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                positions.append((x, y))

        return positions

    def is_position_free(self, position):
        """Checks whether a cell is free for food or power-ups."""
        return (
            position not in self.snake
            and position not in self.obstacles
            and position != self.food
            and position != self.poison_food
            and position != self.powerup
        )

    def random_free_cell(self):
        """Returns a random free cell."""
        while True:
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            position = (x, y)

            if self.is_position_free(position):
                return position

    def generate_food(self):
        """Generates normal food with random weight and timer."""
        self.food = self.random_free_cell()
        self.food_weight = random.choice([1, 1, 1, 2, 2, 3])
        self.food_spawn_time = pygame.time.get_ticks()

    def generate_poison_food(self):
        """Generates poison food."""
        self.poison_food = self.random_free_cell()
        self.poison_spawn_time = pygame.time.get_ticks()

    def maybe_generate_powerup(self):
        """
        Spawns one temporary power-up.
        Only one power-up can be on the field at a time.
        """
        if self.powerup is not None:
            return

        # Random chance each frame. Low value prevents too many power-ups.
        if random.random() < 0.004:
            self.powerup = self.random_free_cell()
            self.powerup_type = random.choice(["Speed Boost", "Slow Motion", "Shield"])
            self.powerup_spawn_time = pygame.time.get_ticks()

    def generate_obstacles_for_level(self):
        """
        Generates static obstacles from level 3.
        This function tries to avoid trapping the snake by not placing
        blocks close to the snake head.
        """
        if self.level < 3:
            self.obstacles = []
            return

        head_x, head_y = self.snake[0]
        new_obstacles = []

        obstacle_count = min(6 + self.level * 2, 35)

        attempts = 0
        while len(new_obstacles) < obstacle_count and attempts < 500:
            attempts += 1

            x = random.randrange(CELL_SIZE, WIDTH - CELL_SIZE, CELL_SIZE)
            y = random.randrange(CELL_SIZE, HEIGHT - CELL_SIZE, CELL_SIZE)
            position = (x, y)

            # Do not place obstacles too close to snake head.
            distance_from_head = abs(x - head_x) + abs(y - head_y)

            if distance_from_head < CELL_SIZE * 5:
                continue

            if position in self.snake or position == self.food or position == self.poison_food:
                continue

            if position in new_obstacles:
                continue

            new_obstacles.append(position)

        self.obstacles = new_obstacles

    def update_level(self):
        """Increases level every N foods and updates speed."""
        new_level = self.foods_eaten // FOODS_PER_LEVEL + 1

        if new_level > self.level:
            self.level = new_level
            self.base_speed += 2
            self.generate_obstacles_for_level()

    def activate_powerup(self, powerup_type):
        """Activates collected power-up."""
        now = pygame.time.get_ticks()

        if self.active_powerup is not None:
            return

        if powerup_type == "Speed Boost":
            self.active_powerup = "Speed Boost"
            self.powerup_end_time = now + POWERUP_EFFECT_DURATION

        elif powerup_type == "Slow Motion":
            self.active_powerup = "Slow Motion"
            self.powerup_end_time = now + POWERUP_EFFECT_DURATION

        elif powerup_type == "Shield":
            self.active_powerup = "Shield"
            self.shield_ready = True
            self.powerup_end_time = 0

    def update_powerup_effect(self):
        """Applies active power-up effects and timers."""
        now = pygame.time.get_ticks()

        if self.active_powerup == "Speed Boost":
            self.current_speed = self.base_speed + 4

            if now >= self.powerup_end_time:
                self.active_powerup = None
                self.current_speed = self.base_speed

        elif self.active_powerup == "Slow Motion":
            self.current_speed = max(4, self.base_speed - 4)

            if now >= self.powerup_end_time:
                self.active_powerup = None
                self.current_speed = self.base_speed

        elif self.active_powerup == "Shield":
            self.current_speed = self.base_speed

        else:
            self.current_speed = self.base_speed

    def check_timers(self):
        """Checks food, poison food, and power-up timers."""
        now = pygame.time.get_ticks()

        # Normal food disappears after timer.
        if now - self.food_spawn_time >= FOOD_LIFETIME:
            self.generate_food()

        # Poison food also changes position after timer.
        if now - self.poison_spawn_time >= POISON_LIFETIME:
            self.generate_poison_food()

        # Power-up disappears after 8 seconds if not collected.
        if self.powerup is not None and now - self.powerup_spawn_time >= POWERUP_FIELD_LIFETIME:
            self.powerup = None
            self.powerup_type = None

        self.maybe_generate_powerup()

    def handle_deadly_collision(self):
        """
        Handles collision with wall, self, or obstacle.
        Shield ignores the next collision once.
        """
        if self.active_powerup == "Shield" and self.shield_ready:
            self.shield_ready = False
            self.active_powerup = None
            return False

        return True

    def shorten_snake(self, segments):
        """Shortens the snake by removing segments from tail."""
        for _ in range(segments):
            if len(self.snake) > 0:
                self.snake.pop()

        if len(self.snake) <= 1:
            self.game_over = True

    def move_snake(self):
        """Moves snake by one cell and checks collisions."""
        self.direction = self.next_direction

        head_x, head_y = self.snake[0]

        if self.direction == "UP":
            head_y -= CELL_SIZE
        elif self.direction == "DOWN":
            head_y += CELL_SIZE
        elif self.direction == "LEFT":
            head_x -= CELL_SIZE
        elif self.direction == "RIGHT":
            head_x += CELL_SIZE

        new_head = (head_x, head_y)

        # Border collision.
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            if self.handle_deadly_collision():
                self.game_over = True
                return
            else:
                # If shield saves the player, keep snake in bounds.
                new_head = self.snake[0]

        # Self collision.
        if new_head in self.snake:
            if self.handle_deadly_collision():
                self.game_over = True
                return

        # Obstacle collision.
        if new_head in self.obstacles:
            if self.handle_deadly_collision():
                self.game_over = True
                return

        self.snake.insert(0, new_head)

        # Normal food.
        if new_head == self.food:
            self.score += self.food_weight
            self.foods_eaten += 1
            self.generate_food()
            self.update_level()

        # Poison food.
        elif new_head == self.poison_food:
            self.score = max(0, self.score - 1)
            self.generate_poison_food()
            self.shorten_snake(2)

        # Power-up.
        elif self.powerup is not None and new_head == self.powerup:
            self.activate_powerup(self.powerup_type)
            self.powerup = None
            self.powerup_type = None
            self.snake.pop()

        else:
            # If no food is eaten, remove tail to keep same length.
            self.snake.pop()

    def save_result(self):
        """Saves final result to PostgreSQL."""
        if not self.saved:
            self.database.save_game_session(self.username, self.score, self.level)
            self.saved = True

    def update(self):
        """Updates one game frame."""
        self.update_powerup_effect()
        self.check_timers()
        self.move_snake()

        if self.game_over:
            self.save_result()

    def draw_grid(self):
        """Draws grid overlay."""
        if not self.show_grid:
            return

        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, (35, 35, 35), (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, (35, 35, 35), (0, y), (WIDTH, y))

    def draw_snake(self):
        """Draws snake body."""
        for index, segment in enumerate(self.snake):
            rect = pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE)

            if index == 0:
                pygame.draw.rect(screen, YELLOW, rect, border_radius=4)
            else:
                pygame.draw.rect(screen, self.snake_color, rect, border_radius=4)

            pygame.draw.rect(screen, DARK_GREEN, rect, 2, border_radius=4)

    def draw_food(self):
        """Draws normal weighted food."""
        rect = pygame.Rect(self.food[0], self.food[1], CELL_SIZE, CELL_SIZE)

        if self.food_weight == 1:
            color = RED
        elif self.food_weight == 2:
            color = BLUE
        else:
            color = YELLOW

        pygame.draw.rect(screen, color, rect, border_radius=6)

        text = FONT_SMALL.render(str(self.food_weight), True, BLACK)
        screen.blit(
            text,
            (
                self.food[0] + CELL_SIZE // 2 - text.get_width() // 2,
                self.food[1] + CELL_SIZE // 2 - text.get_height() // 2
            )
        )

    def draw_poison_food(self):
        """Draws poison food."""
        rect = pygame.Rect(self.poison_food[0], self.poison_food[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, DARK_RED, rect, border_radius=6)

        text = FONT_SMALL.render("P", True, WHITE)
        screen.blit(
            text,
            (
                self.poison_food[0] + CELL_SIZE // 2 - text.get_width() // 2,
                self.poison_food[1] + CELL_SIZE // 2 - text.get_height() // 2
            )
        )

    def draw_powerup(self):
        """Draws field power-up."""
        if self.powerup is None:
            return

        if self.powerup_type == "Speed Boost":
            color = ORANGE
            label = "B"
        elif self.powerup_type == "Slow Motion":
            color = CYAN
            label = "S"
        else:
            color = PURPLE
            label = "H"

        rect = pygame.Rect(self.powerup[0], self.powerup[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect, border_radius=6)

        text = FONT_SMALL.render(label, True, BLACK)
        screen.blit(
            text,
            (
                self.powerup[0] + CELL_SIZE // 2 - text.get_width() // 2,
                self.powerup[1] + CELL_SIZE // 2 - text.get_height() // 2
            )
        )

    def draw_obstacles(self):
        """Draws static obstacle blocks."""
        for block in self.obstacles:
            rect = pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 1)

    def draw_hud(self):
        """Draws score, level, personal best, and timers."""
        score_text = FONT.render(f"Score: {self.score}", True, WHITE)
        level_text = FONT.render(f"Level: {self.level}", True, WHITE)
        best_text = FONT.render(f"Personal Best: {self.personal_best}", True, YELLOW)

        screen.blit(score_text, (15, 10))
        screen.blit(level_text, (15, 40))
        screen.blit(best_text, (15, 70))

        # Food timer.
        now = pygame.time.get_ticks()
        food_time = max(0, (FOOD_LIFETIME - (now - self.food_spawn_time)) // 1000 + 1)
        food_timer = FONT_SMALL.render(f"Food: {food_time}s", True, WHITE)
        screen.blit(food_timer, (15, 105))

        if self.active_powerup is None:
            power_text = FONT_SMALL.render("Power-up: none", True, WHITE)
        elif self.active_powerup == "Shield":
            power_text = FONT_SMALL.render("Power-up: Shield ready", True, PURPLE)
        else:
            remaining = max(0, (self.powerup_end_time - now) // 1000 + 1)
            power_text = FONT_SMALL.render(f"Power-up: {self.active_powerup} {remaining}s", True, CYAN)

        screen.blit(power_text, (15, 130))

        db_status = "DB: connected" if self.database.available else "DB: offline"
        db_color = GREEN if self.database.available else RED
        db_text = FONT_SMALL.render(db_status, True, db_color)
        screen.blit(db_text, (WIDTH - db_text.get_width() - 15, 15))

    def draw(self):
        """Draws full gameplay screen."""
        screen.fill(BLACK)
        self.draw_grid()
        self.draw_obstacles()
        self.draw_food()
        self.draw_poison_food()
        self.draw_powerup()
        self.draw_snake()
        self.draw_hud()


# ============================================================
# Screens
# ============================================================

def game_loop(username, settings, database):
    """Runs the gameplay loop."""
    game = SnakeGame(username, settings, database)

    # Movement happens based on speed, not every visual frame.
    last_move_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                database.close()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_UP and game.direction != "DOWN":
                    game.next_direction = "UP"
                elif event.key == pygame.K_DOWN and game.direction != "UP":
                    game.next_direction = "DOWN"
                elif event.key == pygame.K_LEFT and game.direction != "RIGHT":
                    game.next_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and game.direction != "LEFT":
                    game.next_direction = "RIGHT"

        now = pygame.time.get_ticks()
        move_delay = max(50, int(1000 / game.current_speed))

        if now - last_move_time >= move_delay and not game.game_over:
            game.update()
            last_move_time = now

        game.draw()

        if game.game_over:
            game_over_screen(game, settings, database)
            return

        pygame.display.update()
        clock.tick(FPS)


def main_menu(settings, database):
    """Main menu screen."""
    play_btn = Button(WIDTH // 2 - 130, 250, 260, 55, "Play")
    leaderboard_btn = Button(WIDTH // 2 - 130, 320, 260, 55, "Leaderboard")
    settings_btn = Button(WIDTH // 2 - 130, 390, 260, 55, "Settings")
    quit_btn = Button(WIDTH // 2 - 130, 460, 260, 55, "Quit")

    while True:
        screen.fill(BLACK)
        draw_center_text("TSIS 4 SNAKE", FONT_TITLE, YELLOW, 100)
        draw_center_text("Database Integration & Advanced Gameplay", FONT_SMALL, LIGHT_GRAY, 165)

        play_btn.draw()
        leaderboard_btn.draw()
        settings_btn.draw()
        quit_btn.draw()

        db_status = "PostgreSQL connected" if database.available else "PostgreSQL offline"
        db_color = GREEN if database.available else RED
        draw_center_text(db_status, FONT_SMALL, db_color, 560)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                database.close()
                pygame.quit()
                sys.exit()

            if play_btn.is_clicked(event):
                username = username_input_screen()
                if username is not None:
                    game_loop(username, settings, database)

            elif leaderboard_btn.is_clicked(event):
                leaderboard_screen(database)

            elif settings_btn.is_clicked(event):
                settings_screen(settings)

            elif quit_btn.is_clicked(event):
                database.close()
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)


def game_over_screen(game, settings, database):
    """Game Over screen."""
    retry_btn = Button(WIDTH // 2 - 130, 510, 260, 55, "Retry")
    menu_btn = Button(WIDTH // 2 - 130, 585, 260, 55, "Main Menu")

    new_best = max(game.personal_best, game.score)

    while True:
        screen.fill(BLACK)

        draw_center_text("GAME OVER", FONT_TITLE, RED, 100)
        draw_center_text(f"Player: {game.username}", FONT, WHITE, 210)
        draw_center_text(f"Final Score: {game.score}", FONT, YELLOW, 250)
        draw_center_text(f"Level Reached: {game.level}", FONT, WHITE, 290)
        draw_center_text(f"Personal Best: {new_best}", FONT, YELLOW, 330)

        if not database.available:
            draw_center_text("Database offline: score was not saved", FONT_SMALL, RED, 380)

        retry_btn.draw()
        menu_btn.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                database.close()
                pygame.quit()
                sys.exit()

            if retry_btn.is_clicked(event):
                game_loop(game.username, settings, database)
                return

            if menu_btn.is_clicked(event):
                return

        pygame.display.update()
        clock.tick(FPS)


def leaderboard_screen(database):
    """Leaderboard screen: top 10 from PostgreSQL."""
    back_btn = Button(WIDTH // 2 - 130, 640, 260, 55, "Back")

    while True:
        screen.fill(BLACK)

        draw_center_text("Leaderboard", FONT_BIG, YELLOW, 60)

        if not database.available:
            draw_center_text("Database is offline.", FONT, RED, 250)
            draw_center_text("Check PostgreSQL and config.py.", FONT_SMALL, LIGHT_GRAY, 290)
        else:
            scores = database.get_top_scores(10)

            header = FONT_SMALL.render("Rank   Username        Score     Level     Date", True, WHITE)
            screen.blit(header, (70, 145))

            if not scores:
                draw_center_text("No scores yet.", FONT, LIGHT_GRAY, 260)
            else:
                y = 185
                for index, row in enumerate(scores, start=1):
                    username, score, level, played_at = row
                    date_text = played_at.strftime("%Y-%m-%d")
                    line = f"{index:<5}  {username[:13]:<13}  {score:<8}  {level:<7}  {date_text}"
                    text = FONT_SMALL.render(line, True, WHITE)
                    screen.blit(text, (70, y))
                    y += 38

        back_btn.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                database.close()
                pygame.quit()
                sys.exit()

            if back_btn.is_clicked(event):
                return

        pygame.display.update()
        clock.tick(FPS)


def settings_screen(settings):
    """Settings screen with JSON saving."""
    color_options = [
        [60, 210, 90],
        [70, 140, 240],
        [250, 220, 70],
        [160, 90, 240],
        [255, 150, 40]
    ]

    save_back_btn = Button(WIDTH // 2 - 130, 590, 260, 55, "Save & Back")

    while True:
        screen.fill(BLACK)
        draw_center_text("Settings", FONT_BIG, WHITE, 80)

        grid_text = f"Grid Overlay: {'ON' if settings['grid'] else 'OFF'}"
        sound_text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color_text = f"Snake Color: {settings['snake_color']}"

        grid_btn = Button(WIDTH // 2 - 180, 210, 360, 55, grid_text)
        sound_btn = Button(WIDTH // 2 - 180, 285, 360, 55, sound_text)
        color_btn = Button(WIDTH // 2 - 180, 360, 360, 55, color_text)

        grid_btn.draw()
        sound_btn.draw()
        color_btn.draw()

        # Preview selected snake color.
        preview_color = tuple(settings["snake_color"])
        pygame.draw.rect(screen, preview_color, (WIDTH // 2 - 40, 455, 80, 40), border_radius=8)
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 40, 455, 80, 40), 2, border_radius=8)

        save_back_btn.draw()

        draw_center_text("Settings are saved to settings.json", FONT_SMALL, LIGHT_GRAY, 520)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                pygame.quit()
                sys.exit()

            if grid_btn.is_clicked(event):
                settings["grid"] = not settings["grid"]

            elif sound_btn.is_clicked(event):
                settings["sound"] = not settings["sound"]

            elif color_btn.is_clicked(event):
                current_index = color_options.index(settings["snake_color"]) if settings["snake_color"] in color_options else 0
                settings["snake_color"] = color_options[(current_index + 1) % len(color_options)]

            elif save_back_btn.is_clicked(event):
                save_settings(settings)
                return

        pygame.display.update()
        clock.tick(FPS)


def run():
    """Program entry point."""
    settings = load_settings()
    database = Database()
    main_menu(settings, database)
