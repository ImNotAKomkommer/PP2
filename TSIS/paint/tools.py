# tools.py
# Helper functions for TSIS 2 Paint Application.
# Contains drawing shape helpers and flood-fill implementation.

import pygame
import math
from collections import deque


def get_square_rect(start, end):
    """
    Creates a square rectangle using start and end points.
    The square side is based on the smaller mouse movement direction.
    """
    sx, sy = start
    ex, ey = end

    dx = ex - sx
    dy = ey - sy

    side = min(abs(dx), abs(dy))

    if dx < 0:
        sx -= side

    if dy < 0:
        sy -= side

    return pygame.Rect(sx, sy, side, side)


def get_right_triangle_points(start, end):
    """
    Creates a right triangle using start and end points.
    The triangle is based on an invisible rectangle.
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
    Height is calculated using formula: side * sqrt(3) / 2.
    """
    sx, sy = start
    ex, ey = end

    side = ex - sx
    direction = 1

    if side < 0:
        direction = -1

    side = abs(side)
    height = side * math.sqrt(3) / 2

    point1 = (sx, sy)
    point2 = (sx + side * direction, sy)
    point3 = (sx + side * direction / 2, sy - height)

    return [point1, point2, point3]


def get_rhombus_points(start, end):
    """
    Creates a rhombus inside an invisible rectangle.
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


def get_circle_radius(start, end):
    """
    Calculates radius for circle drawing.
    """
    sx, sy = start
    ex, ey = end

    return int(math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2))


def draw_shape(surface, tool, start, end, color, thickness):
    """
    Draws a selected shape on the given surface.

    Used for:
    - rectangle
    - circle
    - square
    - right triangle
    - equilateral triangle
    - rhombus
    - straight line
    """
    if start is None or end is None:
        return

    if tool == "line":
        pygame.draw.line(surface, color, start, end, thickness)

    elif tool == "rectangle":
        rect = pygame.Rect(start[0], start[1], end[0] - start[0], end[1] - start[1])
        rect.normalize()
        pygame.draw.rect(surface, color, rect, thickness)

    elif tool == "circle":
        radius = get_circle_radius(start, end)
        pygame.draw.circle(surface, color, start, radius, thickness)

    elif tool == "square":
        rect = get_square_rect(start, end)
        pygame.draw.rect(surface, color, rect, thickness)

    elif tool == "right_triangle":
        points = get_right_triangle_points(start, end)
        pygame.draw.polygon(surface, color, points, thickness)

    elif tool == "equilateral_triangle":
        points = get_equilateral_triangle_points(start, end)
        pygame.draw.polygon(surface, color, points, thickness)

    elif tool == "rhombus":
        points = get_rhombus_points(start, end)
        pygame.draw.polygon(surface, color, points, thickness)


def flood_fill(surface, start_pos, fill_color):
    """
    Flood-fill implementation using pygame.Surface.get_at() and set_at().

    The algorithm:
    1. Reads the target color at the clicked pixel.
    2. Replaces connected pixels of the same color with fill_color.
    3. Stops when neighboring pixels have a different color.

    Exact color matching is used.
    """
    width, height = surface.get_size()
    x, y = start_pos

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))
    replacement_color = pygame.Color(fill_color)

    # If clicked color is already selected color, no fill is needed.
    if target_color == replacement_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        current_x, current_y = queue.popleft()

        if current_x < 0 or current_x >= width or current_y < 0 or current_y >= height:
            continue

        if surface.get_at((current_x, current_y)) != target_color:
            continue

        surface.set_at((current_x, current_y), replacement_color)

        queue.append((current_x + 1, current_y))
        queue.append((current_x - 1, current_y))
        queue.append((current_x, current_y + 1))
        queue.append((current_x, current_y - 1))
