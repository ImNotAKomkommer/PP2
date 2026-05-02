# paint.py
# TSIS 2: Paint Application — Extended Drawing Tools.
# Uses only Pygame built-in drawing, font, image saving, and surface pixel operations.

import pygame
import sys
from datetime import datetime

from tools import draw_shape, flood_fill


pygame.init()

# -----------------------------
# Window settings
# -----------------------------
WIDTH = 1100
HEIGHT = 760
TOOLBAR_HEIGHT = 120
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 Paint Application")

clock = pygame.time.Clock()

# -----------------------------
# Colors
# -----------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (75, 75, 75)
LIGHT_GRAY = (220, 220, 220)

RED = (230, 50, 50)
GREEN = (50, 200, 80)
BLUE = (60, 120, 230)
YELLOW = (250, 220, 50)
PURPLE = (160, 90, 240)
ORANGE = (255, 150, 40)

# -----------------------------
# Fonts
# -----------------------------
FONT_SMALL = pygame.font.SysFont("Verdana", 15)
FONT = pygame.font.SysFont("Verdana", 18)
FONT_TEXT_TOOL = pygame.font.SysFont("Arial", 28)

# -----------------------------
# Canvas
# -----------------------------
CANVAS_WIDTH = WIDTH
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

# -----------------------------
# Tool state
# -----------------------------
current_tool = "pencil"
current_color = BLACK

# Brush size levels from task:
# small = 2 px, medium = 5 px, large = 10 px
brush_sizes = {
    "small": 2,
    "medium": 5,
    "large": 10
}

brush_size_name = "medium"
brush_size = brush_sizes[brush_size_name]

drawing_shape = False
shape_start = None

# Used by pencil tool to draw continuous lines.
last_mouse_pos = None

# Text tool state.
text_mode = False
text_position = None
text_buffer = ""

# Save message state.
save_message = ""
save_message_time = 0


# ============================================================
# Coordinate helpers
# ============================================================

def is_on_canvas(mouse_pos):
    """Checks whether mouse position is inside canvas area."""
    return mouse_pos[1] >= TOOLBAR_HEIGHT


def to_canvas_pos(mouse_pos):
    """Converts screen coordinates to canvas coordinates."""
    x, y = mouse_pos
    return x, y - TOOLBAR_HEIGHT


def to_screen_pos(canvas_pos):
    """Converts canvas coordinates to screen coordinates."""
    x, y = canvas_pos
    return x, y + TOOLBAR_HEIGHT


# ============================================================
# Drawing UI
# ============================================================

def draw_toolbar():
    """Draws toolbar with instructions, selected tool, selected color, and brush size."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 3)

    line1 = "Tools: P Pencil | L Line | R Rect | C Circle | S Square | T Text | F Fill | E Eraser"
    line2 = "Shapes: A Right Triangle | Q Equilateral Triangle | D Rhombus"
    line3 = "Brush Size: 1 Small(2px) | 2 Medium(5px) | 3 Large(10px) | Ctrl+S Save PNG"
    line4 = "Colors: K Black | W White | Red: Z | Green: X | Blue: V | Yellow: Y | Purple: U | Orange: O"

    screen.blit(FONT_SMALL.render(line1, True, BLACK), (15, 8))
    screen.blit(FONT_SMALL.render(line2, True, BLACK), (15, 32))
    screen.blit(FONT_SMALL.render(line3, True, BLACK), (15, 56))
    screen.blit(FONT_SMALL.render(line4, True, BLACK), (15, 80))

    status = f"Current Tool: {current_tool} | Brush: {brush_size_name} ({brush_size}px)"
    screen.blit(FONT.render(status, True, BLACK), (610, 15))

    # Color preview.
    pygame.draw.rect(screen, current_color, (820, 50, 60, 35), border_radius=6)
    pygame.draw.rect(screen, BLACK, (820, 50, 60, 35), 2, border_radius=6)

    screen.blit(FONT_SMALL.render("Color", True, BLACK), (828, 88))

    # Save message.
    if save_message:
        elapsed = pygame.time.get_ticks() - save_message_time
        if elapsed < 2500:
            screen.blit(FONT_SMALL.render(save_message, True, BLUE), (610, 88))


def draw_text_preview():
    """Draws temporary text while user is typing."""
    if not text_mode or text_position is None:
        return

    screen_pos = to_screen_pos(text_position)

    # Draw cursor box.
    pygame.draw.rect(screen, (245, 245, 245), (screen_pos[0], screen_pos[1], 260, 34))
    pygame.draw.rect(screen, BLUE, (screen_pos[0], screen_pos[1], 260, 34), 2)

    shown_text = text_buffer + "|"
    text_surface = FONT_TEXT_TOOL.render(shown_text, True, current_color)
    screen.blit(text_surface, (screen_pos[0] + 5, screen_pos[1] + 2))


def draw_shape_preview(mouse_pos):
    """Draws live preview for line and shape tools while dragging."""
    if not drawing_shape or shape_start is None:
        return

    preview_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.SRCALPHA)
    end_pos = to_canvas_pos(mouse_pos)

    draw_shape(
        preview_surface,
        current_tool,
        shape_start,
        end_pos,
        current_color,
        brush_size
    )

    screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))


# ============================================================
# Save canvas
# ============================================================

def save_canvas():
    """
    Saves current canvas as PNG file.
    Filename includes timestamp to avoid overwriting.
    """
    global save_message, save_message_time

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paint_save_{timestamp}.png"

    pygame.image.save(canvas, filename)

    save_message = f"Saved as {filename}"
    save_message_time = pygame.time.get_ticks()


# ============================================================
# Text tool
# ============================================================

def confirm_text():
    """Renders typed text permanently onto canvas."""
    global text_mode, text_buffer, text_position

    if text_mode and text_position is not None and text_buffer:
        text_surface = FONT_TEXT_TOOL.render(text_buffer, True, current_color)
        canvas.blit(text_surface, text_position)

    text_mode = False
    text_buffer = ""
    text_position = None


def cancel_text():
    """Cancels current text input."""
    global text_mode, text_buffer, text_position

    text_mode = False
    text_buffer = ""
    text_position = None


# ============================================================
# Keyboard handling
# ============================================================

def handle_keyboard(event):
    """
    Handles keyboard shortcuts for:
    - tools
    - colors
    - brush sizes
    - saving
    - text input
    """
    global current_tool, current_color
    global brush_size_name, brush_size
    global text_buffer

    keys = pygame.key.get_pressed()

    # Ctrl+S saves canvas.
    if event.key == pygame.K_s and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
        save_canvas()
        return

    # Text mode uses keyboard for typing.
    if text_mode:
        if event.key == pygame.K_RETURN:
            confirm_text()
            return

        if event.key == pygame.K_ESCAPE:
            cancel_text()
            return

        if event.key == pygame.K_BACKSPACE:
            text_buffer = text_buffer[:-1]
            return

        if event.unicode and event.unicode.isprintable():
            text_buffer += event.unicode
            return

    # Tool shortcuts.
    if event.key == pygame.K_p:
        current_tool = "pencil"

    elif event.key == pygame.K_l:
        current_tool = "line"

    elif event.key == pygame.K_r:
        current_tool = "rectangle"

    elif event.key == pygame.K_c:
        current_tool = "circle"

    elif event.key == pygame.K_s:
        current_tool = "square"

    elif event.key == pygame.K_a:
        current_tool = "right_triangle"

    elif event.key == pygame.K_q:
        current_tool = "equilateral_triangle"

    elif event.key == pygame.K_d:
        current_tool = "rhombus"

    elif event.key == pygame.K_f:
        current_tool = "fill"

    elif event.key == pygame.K_t:
        current_tool = "text"

    elif event.key == pygame.K_e:
        current_tool = "eraser"

    # Brush size shortcuts.
    elif event.key == pygame.K_1:
        brush_size_name = "small"
        brush_size = brush_sizes[brush_size_name]

    elif event.key == pygame.K_2:
        brush_size_name = "medium"
        brush_size = brush_sizes[brush_size_name]

    elif event.key == pygame.K_3:
        brush_size_name = "large"
        brush_size = brush_sizes[brush_size_name]

    # Color shortcuts.
    elif event.key == pygame.K_k:
        current_color = BLACK

    elif event.key == pygame.K_w:
        current_color = WHITE

    elif event.key == pygame.K_z:
        current_color = RED

    elif event.key == pygame.K_x:
        current_color = GREEN

    elif event.key == pygame.K_v:
        current_color = BLUE

    elif event.key == pygame.K_y:
        current_color = YELLOW

    elif event.key == pygame.K_u:
        current_color = PURPLE

    elif event.key == pygame.K_o:
        current_color = ORANGE


# ============================================================
# Mouse handling
# ============================================================

def handle_mouse_down(event):
    """Handles mouse press."""
    global drawing_shape, shape_start
    global last_mouse_pos
    global text_mode, text_position, text_buffer

    mouse_pos = event.pos

    if not is_on_canvas(mouse_pos):
        return

    canvas_pos = to_canvas_pos(mouse_pos)

    if current_tool == "pencil":
        last_mouse_pos = canvas_pos

    elif current_tool == "eraser":
        last_mouse_pos = canvas_pos

    elif current_tool == "fill":
        flood_fill(canvas, canvas_pos, current_color)

    elif current_tool == "text":
        # Start text mode at clicked position.
        text_mode = True
        text_position = canvas_pos
        text_buffer = ""

    elif current_tool in [
        "line",
        "rectangle",
        "circle",
        "square",
        "right_triangle",
        "equilateral_triangle",
        "rhombus"
    ]:
        drawing_shape = True
        shape_start = canvas_pos


def handle_mouse_up(event):
    """Handles mouse release."""
    global drawing_shape, shape_start
    global last_mouse_pos

    mouse_pos = event.pos

    if not is_on_canvas(mouse_pos):
        drawing_shape = False
        shape_start = None
        last_mouse_pos = None
        return

    canvas_pos = to_canvas_pos(mouse_pos)

    if drawing_shape and shape_start is not None:
        draw_shape(
            canvas,
            current_tool,
            shape_start,
            canvas_pos,
            current_color,
            brush_size
        )

    drawing_shape = False
    shape_start = None
    last_mouse_pos = None


def handle_continuous_drawing():
    """
    Handles pencil and eraser continuous drawing.

    Pencil uses pygame.draw.line between previous and current mouse positions,
    so the line is smooth and continuous even when the mouse moves quickly.
    """
    global last_mouse_pos

    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if not mouse_pressed[0]:
        return

    if not is_on_canvas(mouse_pos):
        return

    canvas_pos = to_canvas_pos(mouse_pos)

    if current_tool == "pencil":
        if last_mouse_pos is not None:
            pygame.draw.line(canvas, current_color, last_mouse_pos, canvas_pos, brush_size)
        last_mouse_pos = canvas_pos

    elif current_tool == "eraser":
        if last_mouse_pos is not None:
            pygame.draw.line(canvas, WHITE, last_mouse_pos, canvas_pos, brush_size * 2)
        last_mouse_pos = canvas_pos


# ============================================================
# Main loop
# ============================================================

def main():
    """Main program loop."""
    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                handle_keyboard(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_mouse_down(event)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                handle_mouse_up(event)

        handle_continuous_drawing()

        # Draw screen.
        screen.fill(WHITE)
        draw_toolbar()
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        # Live previews are drawn after canvas blit.
        draw_shape_preview(mouse_pos)
        draw_text_preview()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
