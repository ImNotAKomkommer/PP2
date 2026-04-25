import pygame
import sys
import math

pygame.init()

# -----------------------------
# Window settings
# -----------------------------
WIDTH = 900
HEIGHT = 650
TOOLBAR_HEIGHT = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint - Practice 11")

clock = pygame.time.Clock()

# -----------------------------
# Colors
# -----------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (230, 50, 50)
GREEN = (50, 200, 80)
BLUE = (60, 120, 230)
YELLOW = (250, 220, 50)

# -----------------------------
# Font
# -----------------------------
font = pygame.font.SysFont("Verdana", 17)

# -----------------------------
# Paint settings
# -----------------------------
background_color = WHITE
current_color = BLACK
current_tool = "brush"

brush_size = 6

# Shape drawing variables
drawing_shape = False
start_pos = None

# Canvas stores the real drawing
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(background_color)


def get_canvas_pos(mouse_pos):
    """
    Converts screen mouse position to canvas position.
    Canvas starts below toolbar.
    """
    x, y = mouse_pos
    return x, y - TOOLBAR_HEIGHT


def draw_toolbar():
    """Draws toolbar with controls and current settings."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 3)

    line1 = font.render(
        "Tools: 1 Brush | 2 Square | 3 Right Triangle | 4 Equilateral Triangle | 5 Rhombus | C Clear",
        True,
        BLACK
    )

    line2 = font.render(
        "Colors: R Red | G Green | B Blue | Y Yellow | K Black | W White",
        True,
        BLACK
    )

    line3 = font.render(
        f"Current tool: {current_tool} | Current color:",
        True,
        BLACK
    )

    screen.blit(line1, (15, 10))
    screen.blit(line2, (15, 38))
    screen.blit(line3, (15, 64))

    # Show selected color
    pygame.draw.rect(screen, current_color, (360, 63, 35, 20))
    pygame.draw.rect(screen, BLACK, (360, 63, 35, 20), 2)


def get_square_rect(start, end):
    """
    Creates a square rectangle.
    The side length is based on mouse movement.
    """
    sx, sy = start
    ex, ey = end

    dx = ex - sx
    dy = ey - sy

    side = min(abs(dx), abs(dy))

    # Keep direction depending on mouse drag
    if dx < 0:
        sx -= side

    if dy < 0:
        sy -= side

    return pygame.Rect(sx, sy, side, side)


def get_right_triangle_points(start, end):
    """
    Creates points for a right triangle.
    The triangle is based on the rectangle from start to end.
    """
    sx, sy = start
    ex, ey = end

    return [
        (sx, sy),
        (sx, ey),
        (ex, ey)
    ]


def get_equilateral_triangle_points(start, end):
    """
    Creates an equilateral triangle.
    Width is based on mouse drag.
    Height is calculated using formula:
    height = side * sqrt(3) / 2
    """
    sx, sy = start
    ex, ey = end

    side = ex - sx

    # Direction of drawing
    direction = 1
    if side < 0:
        direction = -1

    side = abs(side)
    height = side * math.sqrt(3) / 2

    # Triangle points
    point1 = (sx, sy)
    point2 = (sx + side * direction, sy)
    point3 = (sx + side * direction / 2, sy - height)

    return [point1, point2, point3]


def get_rhombus_points(start, end):
    """
    Creates a rhombus using start and end positions.
    The rhombus is drawn inside an invisible rectangle.
    """
    sx, sy = start
    ex, ey = end

    center_x = (sx + ex) // 2
    center_y = (sy + ey) // 2

    return [
        (center_x, sy),
        (ex, center_y),
        (center_x, ey),
        (sx, center_y)
    ]


def draw_shape(surface, end_mouse_pos, preview=False):
    """
    Draws selected shape on a given surface.
    If preview=True, shape is drawn only as outline.
    """
    if start_pos is None:
        return

    end_pos = get_canvas_pos(end_mouse_pos)

    # In preview mode we draw on the screen, not directly on the canvas.
    # Because screen coordinates include toolbar offset,
    # we need to shift y coordinates down.
    y_offset = TOOLBAR_HEIGHT if preview else 0

    width = 2 if preview else 3

    if current_tool == "square":
        rect = get_square_rect(start_pos, end_pos)

        if preview:
            rect.y += y_offset

        pygame.draw.rect(surface, current_color, rect, width)

    elif current_tool == "right_triangle":
        points = get_right_triangle_points(start_pos, end_pos)

        if preview:
            points = [(x, y + y_offset) for x, y in points]

        pygame.draw.polygon(surface, current_color, points, width)

    elif current_tool == "equilateral_triangle":
        points = get_equilateral_triangle_points(start_pos, end_pos)

        if preview:
            points = [(x, y + y_offset) for x, y in points]

        pygame.draw.polygon(surface, current_color, points, width)

    elif current_tool == "rhombus":
        points = get_rhombus_points(start_pos, end_pos)

        if preview:
            points = [(x, y + y_offset) for x, y in points]

        pygame.draw.polygon(surface, current_color, points, width)


# -----------------------------
# Main loop
# -----------------------------
while True:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # -----------------------------
        # Keyboard controls
        # -----------------------------
        if event.type == pygame.KEYDOWN:
            # Tool selection
            if event.key == pygame.K_1:
                current_tool = "brush"

            elif event.key == pygame.K_2:
                current_tool = "square"

            elif event.key == pygame.K_3:
                current_tool = "right_triangle"

            elif event.key == pygame.K_4:
                current_tool = "equilateral_triangle"

            elif event.key == pygame.K_5:
                current_tool = "rhombus"

            # Clear canvas
            elif event.key == pygame.K_c:
                canvas.fill(background_color)

            # Color selection
            elif event.key == pygame.K_r:
                current_color = RED

            elif event.key == pygame.K_g:
                current_color = GREEN

            elif event.key == pygame.K_b:
                current_color = BLUE

            elif event.key == pygame.K_y:
                current_color = YELLOW

            elif event.key == pygame.K_k:
                current_color = BLACK

            elif event.key == pygame.K_w:
                current_color = WHITE

        # -----------------------------
        # Start drawing shape
        # -----------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and mouse_pos[1] > TOOLBAR_HEIGHT:
                if current_tool in [
                    "square",
                    "right_triangle",
                    "equilateral_triangle",
                    "rhombus"
                ]:
                    drawing_shape = True
                    start_pos = get_canvas_pos(mouse_pos)

        # -----------------------------
        # Finish drawing shape
        # -----------------------------
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing_shape:
                draw_shape(canvas, mouse_pos, preview=False)
                drawing_shape = False
                start_pos = None

    # -----------------------------
    # Brush drawing
    # -----------------------------
    if mouse_pressed[0] and mouse_pos[1] > TOOLBAR_HEIGHT:
        if current_tool == "brush":
            canvas_pos = get_canvas_pos(mouse_pos)
            pygame.draw.circle(canvas, current_color, canvas_pos, brush_size)

    # -----------------------------
    # Draw screen
    # -----------------------------
    screen.fill(WHITE)

    # Draw toolbar
    draw_toolbar()

    # Draw saved canvas
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    # Draw preview shape while mouse is held
    if drawing_shape:
        draw_shape(screen, mouse_pos, preview=True)

    pygame.display.update()
    clock.tick(60)