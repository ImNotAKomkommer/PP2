import pygame
import sys
import math

pygame.init()

# -----------------------------
# Window settings
# -----------------------------
WIDTH = 900
HEIGHT = 650
TOOLBAR_HEIGHT = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint - Practice 10")

clock = pygame.time.Clock()

# -----------------------------
# Colors
# -----------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (90, 90, 90)
RED = (230, 50, 50)
GREEN = (50, 200, 80)
BLUE = (60, 120, 230)
YELLOW = (250, 220, 50)

# -----------------------------
# Font
# -----------------------------
font = pygame.font.SysFont("Verdana", 18)

# -----------------------------
# Paint settings
# -----------------------------
current_color = BLACK
background_color = WHITE
brush_size = 6
eraser_size = 22

# Available tools: brush, rect, circle, eraser
current_tool = "brush"

# Used for rectangle and circle drawing
drawing_shape = False
start_pos = None

# Canvas is a separate surface where the drawing is stored
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(background_color)


def draw_toolbar():
    """Draws toolbar with current tool and color information."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 3)

    info1 = font.render("Tools: 1 Brush | 2 Rectangle | 3 Circle | 4 Eraser | C Clear", True, BLACK)
    info2 = font.render("Colors: R Red | G Green | B Blue | Y Yellow | K Black | W White", True, BLACK)
    info3 = font.render(f"Current tool: {current_tool} | Current color:", True, BLACK)

    screen.blit(info1, (15, 10))
    screen.blit(info2, (15, 35))
    screen.blit(info3, (15, 58))

    # Shows selected color
    pygame.draw.rect(screen, current_color, (350, 57, 30, 18))
    pygame.draw.rect(screen, BLACK, (350, 57, 30, 18), 2)


def get_canvas_position(mouse_pos):
    """
    Converts mouse position from screen coordinates
    to canvas coordinates.
    """
    x, y = mouse_pos
    return x, y - TOOLBAR_HEIGHT


def draw_preview(mouse_pos):
    """
    Draws temporary preview for rectangle or circle.
    This does not affect the real canvas until mouse is released.
    """
    if not drawing_shape or start_pos is None:
        return

    end_pos = get_canvas_position(mouse_pos)
    sx, sy = start_pos
    ex, ey = end_pos

    preview_color = current_color

    # Rectangle preview
    if current_tool == "rect":
        rect = pygame.Rect(sx, sy, ex - sx, ey - sy)
        rect.normalize()
        pygame.draw.rect(screen, preview_color, (rect.x, rect.y + TOOLBAR_HEIGHT, rect.width, rect.height), 3)

    # Circle preview
    elif current_tool == "circle":
        radius = int(math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2))
        pygame.draw.circle(screen, preview_color, (sx, sy + TOOLBAR_HEIGHT), radius, 3)


def apply_shape(end_mouse_pos):
    """
    Draws the final rectangle or circle on the canvas.
    """
    global drawing_shape, start_pos

    if start_pos is None:
        return

    end_pos = get_canvas_position(end_mouse_pos)
    sx, sy = start_pos
    ex, ey = end_pos

    # Draw final rectangle
    if current_tool == "rect":
        rect = pygame.Rect(sx, sy, ex - sx, ey - sy)
        rect.normalize()
        pygame.draw.rect(canvas, current_color, rect, 3)

    # Draw final circle
    elif current_tool == "circle":
        radius = int(math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2))
        pygame.draw.circle(canvas, current_color, (sx, sy), radius, 3)

    drawing_shape = False
    start_pos = None


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
            if event.key == pygame.K_1:
                current_tool = "brush"

            elif event.key == pygame.K_2:
                current_tool = "rect"

            elif event.key == pygame.K_3:
                current_tool = "circle"

            elif event.key == pygame.K_4:
                current_tool = "eraser"

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
        # Mouse controls for shapes
        # -----------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and mouse_pos[1] > TOOLBAR_HEIGHT:
                if current_tool in ["rect", "circle"]:
                    drawing_shape = True
                    start_pos = get_canvas_position(mouse_pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing_shape:
                apply_shape(mouse_pos)

    # -----------------------------
    # Brush and eraser drawing
    # -----------------------------
    if mouse_pressed[0] and mouse_pos[1] > TOOLBAR_HEIGHT:
        canvas_pos = get_canvas_position(mouse_pos)

        if current_tool == "brush":
            pygame.draw.circle(canvas, current_color, canvas_pos, brush_size)

        elif current_tool == "eraser":
            pygame.draw.circle(canvas, background_color, canvas_pos, eraser_size)

    # -----------------------------
    # Drawing screen
    # -----------------------------
    screen.fill(WHITE)

    # Draw toolbar first
    draw_toolbar()

    # Draw canvas below toolbar
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    # Draw shape preview over canvas
    draw_preview(mouse_pos)

    pygame.display.update()
    clock.tick(60)